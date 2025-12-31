"""
Restaurant app views - Handles customer, kitchen, and waiter interfaces
Includes menu display, order management, kitchen dashboard, waiter panel
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.contrib import messages
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import (
    Category, MenuItem, Table, Session, Order, Payment, WaiterAssignment
)


class HomeView(View):
    """
    Home page - redirect to appropriate dashboard based on user role
    """
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect('admin:index')
            elif request.user.groups.filter(name='Kitchen').exists():
                return redirect('kitchen_panel')
            elif request.user.groups.filter(name='Waiter').exists():
                return redirect('waiter_panel')
        return render(request, 'restaurant/home.html')


class MenuView(ListView):
    """
    Customer-facing menu page (accessed via QR code)
    URL: /menu/?table=XX
    """
    model = MenuItem
    template_name = 'restaurant/menu.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        """Get available menu items"""
        return MenuItem.objects.filter(is_available=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get table number from query parameter
        table_number = self.request.GET.get('table')
        
        if table_number:
            try:
                table = Table.objects.get(number=table_number, is_active=True)
                context['table'] = table
                
                # Get or create active session
                session = table.get_active_session()
                if not session:
                    session = Session.objects.create(table=table, status='active')
                context['session'] = session
                
            except Table.DoesNotExist:
                context['error'] = 'Stol topilmadi'
        
        # Group items by category
        categories = Category.objects.filter(is_active=True).prefetch_related('items')
        context['categories'] = categories
        
        return context


class CartView(View):
    """
    Shopping cart view - shows current orders
    """
    def get(self, request):
        table_number = request.GET.get('table')
        
        if not table_number:
            return render(request, 'restaurant/error.html', {'message': 'Stol raqami ko\'rsatilmagan'})
        
        try:
            table = Table.objects.get(number=table_number)
            session = table.get_active_session()
            
            if not session:
                session = Session.objects.create(table=table, status='active')
            
            orders = session.orders.all().select_related('menu_item')
            total = session.get_total_amount()
            
            context = {
                'table': table,
                'session': session,
                'orders': orders,
                'total': total,
            }
            
            return render(request, 'restaurant/cart.html', context)
            
        except Table.DoesNotExist:
            return render(request, 'restaurant/error.html', {'message': 'Stol topilmadi'})


class OrderSubmitView(View):
    """
    Submit new order from cart
    POST endpoint for AJAX requests
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            table_number = data.get('table')
            items = data.get('items', [])
            
            table = Table.objects.get(number=table_number, is_active=True)
            session = table.get_active_session()
            
            if not session:
                session = Session.objects.create(table=table, status='active')
            
            # Create orders
            for item in items:
                menu_item = MenuItem.objects.get(id=item['id'])
                Order.objects.create(
                    session=session,
                    menu_item=menu_item,
                    quantity=item['quantity'],
                    price=menu_item.price,
                    status='pending'
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Buyurtma qabul qilindi',
                'session_id': session.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class BillView(View):
    """
    Display bill/check for a table
    URL: /bill/?table=XX
    """
    def get(self, request):
        table_number = request.GET.get('table')
        
        if not table_number:
            return render(request, 'restaurant/error.html', {'message': 'Stol raqami ko\'rsatilmagan'})
        
        try:
            table = Table.objects.get(number=table_number)
            session = table.get_active_session()
            
            if not session:
                return render(request, 'restaurant/error.html', {'message': 'Faol sessiya topilmadi'})
            
            orders = session.orders.all().select_related('menu_item')
            total = session.get_total_amount()
            payments = session.payments.filter(status='completed')
            paid_amount = sum(p.amount for p in payments)
            remaining = total - paid_amount
            
            context = {
                'table': table,
                'session': session,
                'orders': orders,
                'total': total,
                'paid_amount': paid_amount,
                'remaining': remaining,
            }
            
            return render(request, 'restaurant/bill.html', context)
            
        except Table.DoesNotExist:
            return render(request, 'restaurant/error.html', {'message': 'Stol topilmadi'})


class KitchenPanelView(LoginRequiredMixin, View):
    """
    Kitchen dashboard - shows pending and cooking orders
    Real-time order management for kitchen staff
    """
    def get(self, request):
        # Get orders grouped by status
        pending_orders = Order.objects.filter(
            status='pending'
        ).select_related('session__table', 'menu_item').order_by('created_at')
        
        cooking_orders = Order.objects.filter(
            status='cooking'
        ).select_related('session__table', 'menu_item').order_by('created_at')
        
        done_orders = Order.objects.filter(
            status='done',
            created_at__gte=timezone.now() - timedelta(hours=2)
        ).select_related('session__table', 'menu_item').order_by('-updated_at')
        
        # Statistics
        today = timezone.now().date()
        today_stats = Order.objects.filter(
            created_at__date=today
        ).aggregate(
            total_orders=Count('id'),
            total_items=Sum('quantity')
        )
        
        context = {
            'pending_orders': pending_orders,
            'cooking_orders': cooking_orders,
            'done_orders': done_orders,
            'today_stats': today_stats,
        }
        
        return render(request, 'restaurant/kitchen_panel.html', context)


class UpdateOrderStatusView(LoginRequiredMixin, View):
    """
    Update order status (AJAX endpoint)
    Used by kitchen panel
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('status')
            
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Holat o\'zgartirildi'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class WaiterPanelView(LoginRequiredMixin, View):
    """
    Waiter dashboard - shows tables, sessions, and orders
    Allows waiters to manage tables and close sessions
    """
    def get(self, request):
        # Get all tables with active sessions
        tables = Table.objects.filter(is_active=True).prefetch_related('sessions').order_by('floor', 'number')
        
        # Get active sessions
        active_sessions = Session.objects.filter(status='active').select_related('table', 'waiter')
        
        # Add session info to tables
        for table in tables:
            table.active_session = table.get_active_session()
            if table.active_session:
                table.total_amount = table.active_session.get_total_amount()
                table.order_count = table.active_session.orders.count()
        
        # Statistics for today
        today = timezone.now().date()
        today_stats = Session.objects.filter(
            created_at__date=today,
            status='paid'
        ).aggregate(
            total_sessions=Count('id'),
            total_revenue=Sum('orders__price')
        )
        
        context = {
            'tables': tables,
            'active_sessions': active_sessions,
            'today_stats': today_stats,
        }
        
        return render(request, 'restaurant/waiter_panel.html', context)


class SessionDetailView(LoginRequiredMixin, DetailView):
    """
    Detailed view of a session
    Shows all orders and allows closing session
    """
    model = Session
    template_name = 'restaurant/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.all().select_related('menu_item')
        context['total'] = self.object.get_total_amount()
        context['payments'] = self.object.payments.all()
        return context


class CloseSessionView(LoginRequiredMixin, View):
    """
    Close a session and mark table as available
    """
    def post(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
            
            # Check if all orders are delivered
            pending_orders = session.orders.filter(
                status__in=['pending', 'cooking']
            ).count()
            
            if pending_orders > 0:
                return JsonResponse({
                    'success': False,
                    'message': f'Hali {pending_orders} ta buyurtma tayyor emas'
                }, status=400)
            
            # Close session
            session.close_session()
            
            return JsonResponse({
                'success': True,
                'message': 'Sessiya yopildi'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class CreatePaymentView(LoginRequiredMixin, View):
    """
    Record payment for a session
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            payment_type = data.get('payment_type', 'cash')
            amount = Decimal(data.get('amount', 0))
            
            session = Session.objects.get(id=session_id)
            
            payment = Payment.objects.create(
                session=session,
                payment_type=payment_type,
                amount=amount,
                status='completed',
                processed_by=request.user
            )
            
            # Check if fully paid
            total = session.get_total_amount()
            paid = sum(p.amount for p in session.payments.filter(status='completed'))
            
            if paid >= total:
                session.close_session()
            
            return JsonResponse({
                'success': True,
                'message': 'To\'lov qabul qilindi',
                'payment_id': payment.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class GetKitchenOrdersView(LoginRequiredMixin, View):
    """
    AJAX endpoint for kitchen to get latest orders
    Used for real-time updates (polling)
    """
    def get(self, request):
        pending = list(Order.objects.filter(
            status='pending'
        ).select_related('session__table', 'menu_item').values(
            'id', 'menu_item__name', 'quantity', 'session__table__number',
            'created_at', 'notes'
        ).order_by('created_at'))
        
        cooking = list(Order.objects.filter(
            status='cooking'
        ).select_related('session__table', 'menu_item').values(
            'id', 'menu_item__name', 'quantity', 'session__table__number',
            'created_at', 'notes'
        ).order_by('created_at'))
        
        return JsonResponse({
            'pending': pending,
            'cooking': cooking
        })

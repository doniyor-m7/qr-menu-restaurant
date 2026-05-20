from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from datetime import timedelta
from decimal import Decimal
import json

from .models import Category, MenuItem, Table, Session, Order, Payment, WaiterAssignment


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect('admin:index')
            elif request.user.groups.filter(name='Kitchen').exists():
                return redirect('kitchen_panel')
            elif request.user.groups.filter(name='Waiter').exists():
                return redirect('waiter_panel')
        return render(request, 'restaurant/home.html')


class SetLanguageView(View):
    def get(self, request):
        code = request.GET.get('code', 'uz')
        if code in ('uz', 'ru', 'en'):
            request.session['lang'] = code
        return redirect(request.META.get('HTTP_REFERER', '/'))


class MenuView(ListView):
    model = MenuItem
    template_name = 'restaurant/menu.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_number = self.request.GET.get('table')

        if table_number:
            try:
                table = Table.objects.get(number=table_number, is_active=True)
                context['table'] = table
                session = table.get_active_session()
                if not session:
                    session = Session.objects.create(table=table, status='active')
                context['session'] = session
            except Table.DoesNotExist:
                context['error'] = 'Stol topilmadi'

        context['categories'] = Category.objects.filter(is_active=True).prefetch_related('items')
        return context


class CartView(View):
    def get(self, request):
        table_number = request.GET.get('table')
        if not table_number:
            return render(request, 'restaurant/error.html', {'message': "Stol raqami ko'rsatilmagan"})
        try:
            table = Table.objects.get(number=table_number)
            session = table.get_active_session()
            if not session:
                session = Session.objects.create(table=table, status='active')
            orders = session.orders.all().select_related('menu_item')
            context = {
                'table': table,
                'session': session,
                'orders': orders,
                'total': session.get_total_amount(),
            }
            return render(request, 'restaurant/cart.html', context)
        except Table.DoesNotExist:
            return render(request, 'restaurant/error.html', {'message': 'Stol topilmadi'})


class OrderSubmitView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            table_number = data.get('table')
            items = data.get('items', [])

            if not table_number or not items:
                return JsonResponse({'success': False, 'message': "Ma'lumotlar to'liq emas"}, status=400)

            table = Table.objects.get(number=table_number, is_active=True)
            session = table.get_active_session()
            if not session:
                session = Session.objects.create(table=table, status='active')

            for item in items:
                menu_item = MenuItem.objects.get(id=item['id'], is_available=True)
                qty = max(1, int(item.get('quantity', 1)))
                Order.objects.create(
                    session=session,
                    menu_item=menu_item,
                    quantity=qty,
                    price=menu_item.price,
                    status='pending'
                )

            return JsonResponse({'success': True, 'message': 'Buyurtma qabul qilindi', 'session_id': session.id})

        except Table.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Stol topilmadi'}, status=404)
        except MenuItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': "Taom mavjud emas"}, status=404)
        except (ValueError, KeyError) as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class BillView(View):
    def get(self, request):
        table_number = request.GET.get('table')
        if not table_number:
            return render(request, 'restaurant/error.html', {'message': "Stol raqami ko'rsatilmagan"})
        try:
            table = Table.objects.get(number=table_number)
            session = table.get_active_session()
            if not session:
                return render(request, 'restaurant/error.html', {'message': 'Faol sessiya topilmadi'})
            orders = session.orders.all().select_related('menu_item')
            total = session.get_total_amount()
            payments = session.payments.filter(status='completed')
            paid_amount = sum(p.amount for p in payments)
            context = {
                'table': table,
                'session': session,
                'orders': orders,
                'total': total,
                'paid_amount': paid_amount,
                'remaining': total - paid_amount,
            }
            return render(request, 'restaurant/bill.html', context)
        except Table.DoesNotExist:
            return render(request, 'restaurant/error.html', {'message': 'Stol topilmadi'})


class KitchenPanelView(LoginRequiredMixin, View):
    def get(self, request):
        pending_orders = Order.objects.filter(
            status='pending'
        ).select_related('session__table', 'menu_item').order_by('created_at')

        cooking_orders = Order.objects.filter(
            status='cooking'
        ).select_related('session__table', 'menu_item').order_by('created_at')

        done_orders = Order.objects.filter(
            status='done',
            updated_at__gte=timezone.now() - timedelta(hours=2)
        ).select_related('session__table', 'menu_item').order_by('-updated_at')

        today = timezone.now().date()
        today_stats = Order.objects.filter(
            created_at__date=today,
            status__in=['done', 'delivered']
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
    VALID_TRANSITIONS = {
        'pending': 'cooking',
        'cooking': 'done',
        'done': 'delivered',
    }

    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('status')

            valid_statuses = [s for _, s in Order.STATUS_CHOICES]
            if new_status not in valid_statuses:
                return JsonResponse({'success': False, 'message': 'Noto\'g\'ri holat'}, status=400)

            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()

            return JsonResponse({'success': True, 'message': "Holat o'zgartirildi"})

        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Buyurtma topilmadi'}, status=404)
        except (ValueError, KeyError) as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class WaiterPanelView(LoginRequiredMixin, View):
    def get(self, request):
        tables = Table.objects.filter(is_active=True).order_by('floor', 'number')
        active_sessions = Session.objects.filter(status='active').select_related('table')

        for table in tables:
            table.active_session = table.get_active_session()
            if table.active_session:
                table.total_amount = table.active_session.get_total_amount()
                table.order_count = table.active_session.orders.count()
                table.pending_count = table.active_session.orders.filter(
                    status__in=['pending', 'cooking']
                ).count()

        today = timezone.now().date()
        # Fix: correctly calculate revenue as price × quantity
        today_revenue = Order.objects.filter(
            created_at__date=today,
            session__status='paid'
        ).aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('price') * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )['total'] or Decimal('0')

        today_sessions = Session.objects.filter(
            created_at__date=today,
            status='paid'
        ).count()

        context = {
            'tables': tables,
            'active_sessions': active_sessions,
            'today_revenue': today_revenue,
            'today_sessions': today_sessions,
        }
        return render(request, 'restaurant/waiter_panel.html', context)


class SessionDetailView(LoginRequiredMixin, DetailView):
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
    def post(self, request, session_id):
        try:
            session = get_object_or_404(Session, id=session_id)
            pending_count = session.orders.filter(status__in=['pending', 'cooking']).count()
            if pending_count > 0:
                return JsonResponse({
                    'success': False,
                    'message': f'Hali {pending_count} ta buyurtma tayyor emas'
                }, status=400)
            session.close_session()
            return JsonResponse({'success': True, 'message': 'Sessiya yopildi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            payment_type = data.get('payment_type', 'cash')
            amount = Decimal(str(data.get('amount', 0)))

            if payment_type not in dict(Payment.PAYMENT_TYPE_CHOICES):
                return JsonResponse({'success': False, 'message': "Noto'g'ri to'lov turi"}, status=400)

            session = get_object_or_404(Session, id=session_id)
            payment = Payment.objects.create(
                session=session,
                payment_type=payment_type,
                amount=amount,
                status='completed',
                processed_by=request.user
            )

            total = session.get_total_amount()
            paid = sum(p.amount for p in session.payments.filter(status='completed'))
            if paid >= total:
                session.close_session()

            return JsonResponse({'success': True, 'message': "To'lov qabul qilindi", 'payment_id': payment.id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class GetKitchenOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        def serialize(qs):
            result = []
            for o in qs:
                elapsed = int((timezone.now() - o.created_at).total_seconds() // 60)
                result.append({
                    'id': o.id,
                    'name': o.menu_item.name,
                    'quantity': o.quantity,
                    'table': o.session.table.number,
                    'notes': o.notes,
                    'elapsed': elapsed,
                    'status': o.status,
                })
            return result

        pending = Order.objects.filter(status='pending').select_related('session__table', 'menu_item').order_by('created_at')
        cooking = Order.objects.filter(status='cooking').select_related('session__table', 'menu_item').order_by('created_at')

        return JsonResponse({'pending': serialize(pending), 'cooking': serialize(cooking)})

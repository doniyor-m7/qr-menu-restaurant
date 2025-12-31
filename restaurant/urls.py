"""
URL configuration for restaurant app
Defines all routes for customer, kitchen, and waiter interfaces
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Customer-facing pages (QR code access)
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('bill/', views.BillView.as_view(), name='bill'),
    
    # Order management
    path('order/submit/', views.OrderSubmitView.as_view(), name='order_submit'),
    path('order/update-status/', views.UpdateOrderStatusView.as_view(), name='update_order_status'),
    
    # Kitchen panel
    path('kitchen/', views.KitchenPanelView.as_view(), name='kitchen_panel'),
    path('kitchen/orders/', views.GetKitchenOrdersView.as_view(), name='kitchen_orders_api'),
    
    # Waiter panel
    path('waiter/', views.WaiterPanelView.as_view(), name='waiter_panel'),
    path('waiter/session/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('waiter/session/<int:session_id>/close/', views.CloseSessionView.as_view(), name='close_session'),
    
    # Payment
    path('payment/create/', views.CreatePaymentView.as_view(), name='create_payment'),
]

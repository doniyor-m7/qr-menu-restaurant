"""
Django Admin configuration for Restaurant models
Provides comprehensive admin interface for managing menu, tables, orders, etc.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Category, MenuItem, Table, Session, Order, Payment, WaiterAssignment
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for menu categories"""
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_uz', 'name_ru', 'name_en']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin interface for menu items"""
    list_display = ['name', 'category', 'price', 'is_available', 'is_popular', 'image_preview', 'created_at']
    list_filter = ['category', 'is_available', 'is_popular', 'created_at']
    search_fields = ['name', 'name_uz', 'name_ru', 'name_en', 'description']
    ordering = ['category', 'name']
    list_editable = ['price', 'is_available', 'is_popular']
    readonly_fields = ['image_preview_large', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'name', 'description', 'price', 'preparation_time')
        }),
        ('Ko\'p tillilik', {
            'fields': ('name_uz', 'name_ru', 'name_en'),
            'classes': ('collapse',)
        }),
        ('Rasm', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Holat', {
            'fields': ('is_available', 'is_popular')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Small thumbnail for list view"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Rasm'

    def image_preview_large(self, obj):
        """Large preview for detail view"""
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px;" />', obj.image.url)
        return 'Rasm yuklanmagan'
    image_preview_large.short_description = 'Rasm ko\'rinishi'


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """Admin interface for tables"""
    list_display = ['number', 'floor', 'seats', 'is_active', 'has_qr', 'active_session_link', 'created_at']
    list_filter = ['floor', 'is_active', 'seats']
    search_fields = ['number']
    ordering = ['floor', 'number']
    list_editable = ['is_active']
    readonly_fields = ['qr_preview', 'get_menu_url', 'created_at']
    
    fieldsets = (
        ('Stol ma\'lumotlari', {
            'fields': ('number', 'floor', 'seats', 'is_active')
        }),
        ('QR kod', {
            'fields': ('qr_code', 'qr_preview', 'get_menu_url')
        }),
        ('Tizim', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_qr(self, obj):
        """Display QR code status"""
        if obj.qr_code:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_qr.short_description = 'QR'

    def qr_preview(self, obj):
        """Display QR code preview"""
        if obj.qr_code:
            return format_html('<img src="{}" width="200" />', obj.qr_code.url)
        return 'QR kod mavjud emas'
    qr_preview.short_description = 'QR kod ko\'rinishi'

    def active_session_link(self, obj):
        """Link to active session if exists"""
        session = obj.get_active_session()
        if session:
            url = reverse('admin:restaurant_session_change', args=[session.id])
            return format_html('<a href="{}">Sessiya #{}</a>', url, session.id)
        return '-'
    active_session_link.short_description = 'Faol sessiya'


class OrderInline(admin.TabularInline):
    """Inline orders for session admin"""
    model = Order
    extra = 0
    readonly_fields = ['created_at', 'get_total_price']
    fields = ['menu_item', 'quantity', 'price', 'status', 'notes', 'created_at']
    
    def get_total_price(self, obj):
        if obj.id:
            return f"{obj.get_total_price()} so'm"
        return '-'
    get_total_price.short_description = 'Jami'


class PaymentInline(admin.TabularInline):
    """Inline payments for session admin"""
    model = Payment
    extra = 0
    readonly_fields = ['created_at']
    fields = ['payment_type', 'amount', 'status', 'processed_by', 'created_at']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin interface for dining sessions"""
    list_display = ['id', 'table', 'waiter', 'status', 'total_amount', 'created_at', 'closed_at']
    list_filter = ['status', 'created_at', 'table__floor']
    search_fields = ['table__number', 'waiter__username']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'created_at', 'closed_at']
    inlines = [OrderInline, PaymentInline]
    
    fieldsets = (
        ('Sessiya ma\'lumotlari', {
            'fields': ('table', 'waiter', 'status')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'closed_at')
        }),
        ('Moliyaviy', {
            'fields': ('total_amount',)
        }),
        ('Qo\'shimcha', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def total_amount(self, obj):
        """Display total amount"""
        if obj.id:
            return f"{obj.get_total_amount()} so'm"
        return '-'
    total_amount.short_description = 'Jami summa'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for orders"""
    list_display = ['id', 'session', 'menu_item', 'quantity', 'price', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'menu_item__category']
    search_fields = ['session__table__number', 'menu_item__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'total']
    
    fieldsets = (
        ('Buyurtma', {
            'fields': ('session', 'menu_item', 'quantity', 'price', 'total')
        }),
        ('Holat', {
            'fields': ('status', 'notes')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total(self, obj):
        """Display total price"""
        if obj.id:
            return f"{obj.get_total_price()} so'm"
        return '-'
    total.short_description = 'Jami'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for payments"""
    list_display = ['id', 'session', 'payment_type', 'amount', 'status', 'processed_by', 'created_at']
    list_filter = ['payment_type', 'status', 'created_at']
    search_fields = ['session__table__number', 'transaction_id']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('To\'lov ma\'lumotlari', {
            'fields': ('session', 'payment_type', 'amount', 'status')
        }),
        ('Tranzaksiya', {
            'fields': ('transaction_id', 'processed_by')
        }),
        ('Qo\'shimcha', {
            'fields': ('notes', 'created_at')
        }),
    )


@admin.register(WaiterAssignment)
class WaiterAssignmentAdmin(admin.ModelAdmin):
    """Admin interface for waiter assignments"""
    list_display = ['waiter', 'floor', 'table', 'is_active', 'created_at']
    list_filter = ['is_active', 'floor', 'created_at']
    search_fields = ['waiter__username', 'table__number']
    ordering = ['floor', 'waiter']
    list_editable = ['is_active']


# Customize admin site header
admin.site.site_header = "QR Menu - Restoran boshqaruvi"
admin.site.site_title = "QR Menu Admin"
admin.site.index_title = "Bosh sahifa"

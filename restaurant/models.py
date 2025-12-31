"""
Restaurant app models - Database structure for QR Menu system
Includes: Category, MenuItem, Table, Session, Order, Payment
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    """
    Menu categories (e.g., Main Dishes, Drinks, Desserts)
    """
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (O'zbekcha)", blank=True)
    name_ru = models.CharField(max_length=100, verbose_name="Nomi (Русский)", blank=True)
    name_en = models.CharField(max_length=100, verbose_name="Nomi (English)", blank=True)
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Menu items - individual dishes and drinks
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', verbose_name="Kategoriya")
    name = models.CharField(max_length=200, verbose_name="Taom nomi")
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (O'zbekcha)", blank=True)
    name_ru = models.CharField(max_length=200, verbose_name="Nomi (Русский)", blank=True)
    name_en = models.CharField(max_length=200, verbose_name="Nomi (English)", blank=True)
    description = models.TextField(blank=True, verbose_name="Ta'rif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True, verbose_name="Rasm")
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")
    is_popular = models.BooleanField(default=False, verbose_name="Mashhur")
    preparation_time = models.IntegerField(default=15, verbose_name="Tayyorlash vaqti (daqiqa)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    class Meta:
        verbose_name = "Menyu elementi"
        verbose_name_plural = "Menyu elementlari"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - {self.price} so'm"


class Table(models.Model):
    """
    Restaurant tables with floor information
    """
    number = models.CharField(max_length=10, unique=True, verbose_name="Stol raqami")
    floor = models.IntegerField(default=1, verbose_name="Etaj")
    seats = models.IntegerField(default=4, verbose_name="O'rindiqlar soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name="QR kod")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    class Meta:
        verbose_name = "Stol"
        verbose_name_plural = "Stollar"
        ordering = ['floor', 'number']

    def __str__(self):
        return f"Stol #{self.number} ({self.floor}-etaj)"

    def get_active_session(self):
        """Get current active session for this table"""
        return self.sessions.filter(status='active').first()

    def get_menu_url(self):
        """Generate menu URL for QR code"""
        return f"/menu/?table={self.number}"


class Session(models.Model):
    """
    Dining session per table - tracks orders and payment status
    """
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('paid', 'To\'langan'),
        ('cancelled', 'Bekor qilingan'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='sessions', verbose_name="Stol")
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='sessions', verbose_name="Ofitsant")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Boshlangan vaqt")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Yakunlangan vaqt")
    notes = models.TextField(blank=True, verbose_name="Izohlar")

    class Meta:
        verbose_name = "Sessiya"
        verbose_name_plural = "Sessiyalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sessiya #{self.id} - {self.table} ({self.status})"

    def get_total_amount(self):
        """Calculate total amount for this session"""
        total = sum(order.get_total_price() for order in self.orders.all())
        return Decimal(total)

    def close_session(self):
        """Close the session"""
        self.status = 'paid'
        self.closed_at = timezone.now()
        self.save()


class Order(models.Model):
    """
    Individual order item within a session
    """
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('cooking', 'Tayyorlanmoqda'),
        ('done', 'Tayyor'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilingan'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='orders', verbose_name="Sessiya")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orders', verbose_name="Taom")
    quantity = models.IntegerField(default=1, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma berilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity} - {self.session.table}"

    def save(self, *args, **kwargs):
        """Auto-set price from menu item if not set"""
        if not self.price:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)

    def get_total_price(self):
        """Calculate total price for this order line"""
        return self.price * self.quantity


class Payment(models.Model):
    """
    Payment records for sessions
    """
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Naqd'),
        ('card', 'Terminal'),
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('other', 'Boshqa'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Bajarildi'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('refunded', 'Qaytarildi'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='payments', verbose_name="Sessiya")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='cash', 
                                    verbose_name="To'lov turi")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Summa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="Tranzaksiya ID")
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='processed_payments', verbose_name="Kim qabul qildi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="To'langan vaqt")
    notes = models.TextField(blank=True, verbose_name="Izohlar")

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"To'lov #{self.id} - {self.amount} so'm ({self.payment_type})"


class WaiterAssignment(models.Model):
    """
    Assign waiters to specific floors or tables
    """
    waiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments', 
                               verbose_name="Ofitsant")
    floor = models.IntegerField(null=True, blank=True, verbose_name="Etaj")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='assignments', verbose_name="Stol")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tayinlangan vaqt")

    class Meta:
        verbose_name = "Ofitsant tayinlash"
        verbose_name_plural = "Ofitsant tayinlashlar"
        ordering = ['floor', 'waiter']

    def __str__(self):
        if self.table:
            return f"{self.waiter.username} - {self.table}"
        return f"{self.waiter.username} - {self.floor}-etaj"

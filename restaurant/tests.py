# Tests for restaurant app
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, MenuItem, Table, Session, Order
from decimal import Decimal


class MenuItemTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.item = MenuItem.objects.create(
            category=self.category,
            name="Test Item",
            price=Decimal("10000"),
            is_available=True
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.price, Decimal("10000"))


class TableTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(
            number="1",
            floor=1,
            seats=4,
            is_active=True
        )

    def test_table_creation(self):
        self.assertEqual(self.table.number, "1")
        self.assertEqual(self.table.floor, 1)

    def test_get_menu_url(self):
        url = self.table.get_menu_url()
        self.assertEqual(url, "/menu/?table=1")


class SessionTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number="1", floor=1)
        self.category = Category.objects.create(name="Test")
        self.item = MenuItem.objects.create(
            category=self.category,
            name="Test Item",
            price=Decimal("10000")
        )
        self.session = Session.objects.create(
            table=self.table,
            status='active'
        )

    def test_session_total(self):
        Order.objects.create(
            session=self.session,
            menu_item=self.item,
            quantity=2,
            price=self.item.price
        )
        total = self.session.get_total_amount()
        self.assertEqual(total, Decimal("20000"))

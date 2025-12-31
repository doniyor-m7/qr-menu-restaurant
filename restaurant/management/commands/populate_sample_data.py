"""
Management command to populate database with sample data
Usage: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from restaurant.models import Category, MenuItem, Table
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            MenuItem.objects.all().delete()
            Category.objects.all().delete()
            Table.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Cleared'))

        # Create user groups
        self.stdout.write('Creating user groups...')
        kitchen_group, _ = Group.objects.get_or_create(name='Kitchen')
        waiter_group, _ = Group.objects.get_or_create(name='Waiter')
        self.stdout.write(self.style.SUCCESS('✓ Groups created'))

        # Create sample users
        self.stdout.write('Creating sample users...')
        
        # Admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@qrmenu.uz',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created (admin/admin123)'))
        
        # Kitchen user
        if not User.objects.filter(username='kitchen').exists():
            kitchen_user = User.objects.create_user(
                username='kitchen',
                password='kitchen123',
                first_name='Kitchen',
                last_name='Staff'
            )
            kitchen_user.groups.add(kitchen_group)
            self.stdout.write(self.style.SUCCESS('✓ Kitchen user created (kitchen/kitchen123)'))
        
        # Waiter user
        if not User.objects.filter(username='waiter').exists():
            waiter_user = User.objects.create_user(
                username='waiter',
                password='waiter123',
                first_name='Waiter',
                last_name='Staff'
            )
            waiter_user.groups.add(waiter_group)
            self.stdout.write(self.style.SUCCESS('✓ Waiter user created (waiter/waiter123)'))

        # Create categories
        self.stdout.write('\nCreating categories...')
        categories_data = [
            {'name': 'Osh va suyuq taomlar', 'order': 1},
            {'name': 'Kaboblar', 'order': 2},
            {'name': 'Salatlar', 'order': 3},
            {'name': 'Ichimliklar', 'order': 4},
            {'name': 'Shirinliklar', 'order': 5},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'order': cat_data['order'], 'is_active': True}
            )
            categories[cat_data['name']] = category
            status = 'created' if created else 'exists'
            self.stdout.write(f'  • {cat_data["name"]} ({status})')

        # Create menu items
        self.stdout.write('\nCreating menu items...')
        menu_items = [
            # Osh va suyuq taomlar
            {
                'category': 'Osh va suyuq taomlar',
                'name': 'Osh',
                'description': 'O\'zbekcha milliy taom, guruch va go\'sht',
                'price': Decimal('25000'),
                'is_popular': True,
                'preparation_time': 20,
            },
            {
                'category': 'Osh va suyuq taomlar',
                'name': 'Lagman',
                'description': 'Go\'sht va sabzavotli cho\'zma',
                'price': Decimal('30000'),
                'preparation_time': 25,
            },
            {
                'category': 'Osh va suyuq taomlar',
                'name': 'Mastava',
                'description': 'Go\'sht va sabzavotli sho\'rva',
                'price': Decimal('20000'),
                'preparation_time': 20,
            },
            {
                'category': 'Osh va suyuq taomlar',
                'name': 'Naryn',
                'description': 'Ot go\'shti va cho\'zma',
                'price': Decimal('35000'),
                'preparation_time': 25,
            },
            
            # Kaboblar
            {
                'category': 'Kaboblar',
                'name': 'Qo\'y go\'shti kabobi',
                'description': 'Qo\'y go\'shtidan tayyorlangan kabob (6 dona)',
                'price': Decimal('35000'),
                'is_popular': True,
                'preparation_time': 30,
            },
            {
                'category': 'Kaboblar',
                'name': 'Tovuq kabobi',
                'description': 'Tovuq go\'shtidan tayyorlangan kabob (6 dona)',
                'price': Decimal('28000'),
                'preparation_time': 25,
            },
            {
                'category': 'Kaboblar',
                'name': 'Mol go\'shti kabobi',
                'description': 'Mol go\'shtidan tayyorlangan kabob (6 dona)',
                'price': Decimal('32000'),
                'preparation_time': 30,
            },
            {
                'category': 'Kaboblar',
                'name': 'Jigar kabobi',
                'description': 'Qo\'y jigari kabobi (8 dona)',
                'price': Decimal('30000'),
                'is_popular': True,
                'preparation_time': 20,
            },
            
            # Salatlar
            {
                'category': 'Salatlar',
                'name': 'Achichuk',
                'description': 'Pomidor va piyoz salati',
                'price': Decimal('8000'),
                'preparation_time': 10,
            },
            {
                'category': 'Salatlar',
                'name': 'Olivye',
                'description': 'Rus salati',
                'price': Decimal('12000'),
                'preparation_time': 10,
            },
            {
                'category': 'Salatlar',
                'name': 'Sezar salati',
                'description': 'Tovuq va krutонли salat',
                'price': Decimal('18000'),
                'preparation_time': 15,
            },
            {
                'category': 'Salatlar',
                'name': 'Yunon salati',
                'description': 'Sabzavot va pishloqli salat',
                'price': Decimal('15000'),
                'preparation_time': 10,
            },
            
            # Ichimliklar
            {
                'category': 'Ichimliklar',
                'name': 'Choy (qora)',
                'description': 'Issiq qora choy',
                'price': Decimal('5000'),
                'preparation_time': 5,
            },
            {
                'category': 'Ichimliklar',
                'name': 'Choy (ko\'k)',
                'description': 'Issiq ko\'k choy',
                'price': Decimal('5000'),
                'preparation_time': 5,
            },
            {
                'category': 'Ichimliklar',
                'name': 'Pepsi (0.5L)',
                'description': 'Sovuq ichimlik',
                'price': Decimal('8000'),
                'preparation_time': 2,
            },
            {
                'category': 'Ichimliklar',
                'name': 'Suv (0.5L)',
                'description': 'Toza ichimlik suvi',
                'price': Decimal('3000'),
                'preparation_time': 2,
            },
            {
                'category': 'Ichimliklar',
                'name': 'Sharbat',
                'description': 'O\'zbek milliy ichimlik',
                'price': Decimal('10000'),
                'preparation_time': 5,
            },
            
            # Shirinliklar
            {
                'category': 'Shirinliklar',
                'name': 'Tort (bir bo\'lak)',
                'description': 'Shokoladli tort',
                'price': Decimal('15000'),
                'preparation_time': 5,
            },
            {
                'category': 'Shirinliklar',
                'name': 'Muzqaymoq',
                'description': 'Turli xil ta\'mlar',
                'price': Decimal('12000'),
                'preparation_time': 5,
            },
            {
                'category': 'Shirinliklar',
                'name': 'Paxlava',
                'description': 'Sharqona shirinlik',
                'price': Decimal('10000'),
                'preparation_time': 5,
            },
        ]
        
        created_count = 0
        for item_data in menu_items:
            category = categories[item_data.pop('category')]
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                category=category,
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  • {item.name} - {item.price} so\'m')
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} menu items'))

        # Create tables
        self.stdout.write('\nCreating tables...')
        tables_data = [
            # 1st floor
            *[{'number': str(i), 'floor': 1, 'seats': 4} for i in range(1, 11)],
            # 2nd floor
            *[{'number': str(i), 'floor': 2, 'seats': 4} for i in range(11, 21)],
            # 3rd floor (VIP)
            *[{'number': str(i), 'floor': 3, 'seats': 6} for i in range(21, 26)],
        ]
        
        created_tables = 0
        for table_data in tables_data:
            table, created = Table.objects.get_or_create(
                number=table_data['number'],
                defaults={
                    'floor': table_data['floor'],
                    'seats': table_data['seats'],
                    'is_active': True
                }
            )
            if created:
                created_tables += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_tables} tables'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Menu Items: {MenuItem.objects.count()}')
        self.stdout.write(f'Tables: {Table.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data populated successfully!'))
        self.stdout.write(self.style.WARNING('\nDefault credentials:'))
        self.stdout.write('  Admin:   admin/admin123')
        self.stdout.write('  Kitchen: kitchen/kitchen123')
        self.stdout.write('  Waiter:  waiter/waiter123')

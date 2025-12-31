"""
Management command to generate QR codes for all tables
Usage: python manage.py generate_qr_codes
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from restaurant.models import Table
import qrcode
from io import BytesIO
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Generate QR codes for all tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate QR codes even if they already exist',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        # Get all active tables
        tables = Table.objects.filter(is_active=True)
        
        if not tables.exists():
            self.stdout.write(self.style.WARNING('No active tables found'))
            return
        
        # Get base URL (in production, this should be your domain)
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        
        generated_count = 0
        skipped_count = 0
        
        for table in tables:
            # Skip if QR already exists and force is not set
            if table.qr_code and not force:
                self.stdout.write(f'Skipping table #{table.number} (QR already exists)')
                skipped_count += 1
                continue
            
            # Generate menu URL
            menu_url = f"{base_url}{table.get_menu_url()}"
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(menu_url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Save to model
            filename = f'table_{table.number}_qr.png'
            table.qr_code.save(filename, File(buffer), save=True)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Generated QR code for table #{table.number}')
            )
            generated_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Generated: {generated_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total tables: {tables.count()}'))

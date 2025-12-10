"""
Custom Django management command to sync cars from Odoo

Usage:
    python manage.py sync_cars_from_odoo
"""

from django.core.management.base import BaseCommand
from odoo_integration import OdooConnector, SyncManager


class Command(BaseCommand):
    help = 'Synchronize cars from Odoo to Django'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if cars already exist',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting car synchronization from Odoo...')
        
        try:
            connector = OdooConnector()
            sync = SyncManager(connector)
            
            result = sync.sync_cars_from_odoo()
            
            if result.get('success'):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Sync completed successfully!\n"
                        f"  Created: {result['created']}\n"
                        f"  Updated: {result['updated']}\n"
                        f"  Total: {result['total']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Sync failed: {result.get('error', 'Unknown error')}"
                    )
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"✗ Error: {str(e)}")
            )

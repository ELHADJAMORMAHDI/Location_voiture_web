"""
Example usage of Odoo integration module

This file shows how to use the OdooConnector and SyncManager.
"""

from odoo_integration import OdooConnector, SyncManager
from cars.models import Car, Booking, Customer
import logging

logger = logging.getLogger(__name__)


def example_test_connection():
    """Test connection to Odoo."""
    print("Testing Odoo connection...")
    connector = OdooConnector()
    if connector.test_connection():
        print("✓ Connection successful!")
    else:
        print("✗ Connection failed!")


def example_fetch_cars():
    """Fetch cars from Odoo."""
    print("\nFetching cars from Odoo...")
    connector = OdooConnector()
    cars = connector.fetch_cars()
    
    print(f"Found {len(cars)} cars:")
    for car in cars[:5]:  # Show first 5
        print(f"  - {car.get('name', 'N/A')} (${car.get('daily_rate', 'N/A')}/day)")


def example_sync_cars():
    """Synchronize cars from Odoo to Django."""
    print("\nSyncing cars from Odoo...")
    connector = OdooConnector()
    sync = SyncManager(connector)
    
    result = sync.sync_cars_from_odoo()
    print(f"Sync result: {result}")
    
    # Show Django cars
    print(f"\nDjango has {Car.objects.count()} cars")


def example_create_customer():
    """Create a customer in Odoo."""
    print("\nCreating customer in Odoo...")
    connector = OdooConnector()
    
    customer_data = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'address': '123 Main St',
        'city': 'New York',
        'postal_code': '10001',
    }
    
    odoo_id = connector.create_customer(customer_data)
    print(f"Created customer with Odoo ID: {odoo_id}")


def example_create_booking():
    """Create a booking in Odoo."""
    print("\nCreating booking in Odoo...")
    connector = OdooConnector()
    
    booking_data = {
        'vehicle_id': 1,  # Odoo vehicle ID
        'customer_id': 1,  # Odoo customer ID
        'start_date': '2025-01-15',
        'end_date': '2025-01-20',
        'daily_rate': 50.00,
        'number_of_days': 5,
        'total_cost': 250.00,
    }
    
    booking_id = connector.create_booking(booking_data)
    print(f"Created booking with Odoo ID: {booking_id}")


def example_sync_status():
    """Get synchronization status."""
    print("\nChecking sync status...")
    connector = OdooConnector()
    sync = SyncManager(connector)
    
    status = sync.get_sync_status()
    print(f"Odoo Connected: {status.get('odoo_connected')}")
    print(f"Cars Synced: {status['cars']['synced']}/{status['cars']['total']}")
    print(f"Customers Synced: {status['customers']['synced']}/{status['customers']['total']}")
    print(f"Bookings Synced: {status['bookings']['synced']}/{status['bookings']['total']}")


if __name__ == '__main__':
    # Run examples
    try:
        example_test_connection()
        example_fetch_cars()
        example_sync_cars()
        example_sync_status()
    except Exception as e:
        logger.error(f"Error in examples: {str(e)}")

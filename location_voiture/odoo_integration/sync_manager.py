"""
Sync Manager - Synchronize Django models with Odoo

Handles bidirectional sync of:
- Cars/Vehicles
- Customers
- Bookings
"""

import logging
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from cars.models import Car, Customer, Booking

logger = logging.getLogger(__name__)


class SyncManager:
    """Manage synchronization between Django and Odoo."""
    
    def __init__(self, odoo_connector):
        """
        Initialize sync manager.
        
        Args:
            odoo_connector: OdooConnector instance
        """
        self.odoo = odoo_connector

    def sync_cars_from_odoo(self):
        """
        Sync vehicles from Odoo to Django.
        
        Returns:
            dict: Summary of sync operation
        """
        try:
            vehicles = self.odoo.fetch_cars()
            created = 0
            updated = 0
            
            for vehicle in vehicles:
                # Map Odoo fields to Django model
                car_data = {
                    'registration_number': vehicle.get('license_plate'),
                    'make': vehicle.get('brand', 'Unknown'),
                    'model': vehicle.get('model_id', ['', 'Unknown'])[1],
                    'year': vehicle.get('acquisition_date', datetime.now().year)[:4],
                    'daily_rate': Decimal(str(vehicle.get('daily_rate', 0))),
                    'fuel_type': vehicle.get('fuel_type', 'GASOLINE').upper(),
                    'transmission': vehicle.get('transmission', 'AUTOMATIC').upper(),
                    'seats': vehicle.get('seats', 5),
                    'color': vehicle.get('color', 'Unknown'),
                    'odoo_id': vehicle.get('id'),
                }
                
                # Get or create car
                car, created_flag = Car.objects.get_or_create(
                    registration_number=car_data['registration_number'],
                    defaults=car_data
                )
                
                if created_flag:
                    created += 1
                    logger.info(f"Created car: {car}")
                else:
                    # Update existing car
                    for key, value in car_data.items():
                        setattr(car, key, value)
                    car.save()
                    updated += 1
                    logger.info(f"Updated car: {car}")
            
            summary = {
                'success': True,
                'created': created,
                'updated': updated,
                'total': len(vehicles)
            }
            logger.info(f"Sync complete: {summary}")
            return summary
        
        except Exception as e:
            logger.error(f"Error syncing cars from Odoo: {str(e)}")
            return {'success': False, 'error': str(e)}

    def sync_customer_to_odoo(self, django_customer):
        """
        Sync Django customer to Odoo.
        
        Args:
            django_customer: Customer model instance
            
        Returns:
            int: Odoo customer ID or None
        """
        try:
            customer_data = {
                'full_name': django_customer.user.get_full_name() or django_customer.user.username,
                'email': django_customer.user.email,
                'phone': django_customer.phone_number,
                'address': django_customer.address,
                'city': django_customer.city,
                'postal_code': django_customer.postal_code,
            }
            
            odoo_id = self.odoo.create_customer(customer_data)
            
            if odoo_id:
                django_customer.odoo_id = odoo_id
                django_customer.save()
                logger.info(f"Synced customer to Odoo: {odoo_id}")
            
            return odoo_id
        
        except Exception as e:
            logger.error(f"Error syncing customer to Odoo: {str(e)}")
            return None

    def sync_booking_to_odoo(self, django_booking):
        """
        Sync Django booking to Odoo.
        
        Args:
            django_booking: Booking model instance
            
        Returns:
            int: Odoo booking ID or None
        """
        try:
            # Ensure customer is synced to Odoo
            if not django_booking.customer.odoo_id:
                self.sync_customer_to_odoo(django_booking.customer)
            
            booking_data = {
                'vehicle_id': django_booking.car.odoo_id,
                'customer_id': django_booking.customer.odoo_id,
                'start_date': django_booking.start_date.isoformat(),
                'end_date': django_booking.end_date.isoformat(),
                'daily_rate': float(django_booking.daily_rate),
                'number_of_days': django_booking.number_of_days,
                'total_cost': float(django_booking.total_cost),
                'notes': django_booking.notes,
            }
            
            odoo_id = self.odoo.create_booking(booking_data)
            
            if odoo_id:
                django_booking.odoo_id = odoo_id
                django_booking.save()
                logger.info(f"Synced booking to Odoo: {odoo_id}")
            
            return odoo_id
        
        except Exception as e:
            logger.error(f"Error syncing booking to Odoo: {str(e)}")
            return None

    def get_sync_status(self):
        """
        Get synchronization status.
        
        Returns:
            dict: Status information
        """
        try:
            cars_with_odoo = Car.objects.filter(odoo_id__isnull=False).count()
            customers_with_odoo = Customer.objects.filter(odoo_id__isnull=False).count()
            bookings_with_odoo = Booking.objects.filter(odoo_id__isnull=False).count()
            
            total_cars = Car.objects.count()
            total_customers = Customer.objects.count()
            total_bookings = Booking.objects.count()
            
            return {
                'odoo_connected': self.odoo.test_connection(),
                'cars': {
                    'synced': cars_with_odoo,
                    'total': total_cars,
                    'percentage': (cars_with_odoo / total_cars * 100) if total_cars > 0 else 0
                },
                'customers': {
                    'synced': customers_with_odoo,
                    'total': total_customers,
                    'percentage': (customers_with_odoo / total_customers * 100) if total_customers > 0 else 0
                },
                'bookings': {
                    'synced': bookings_with_odoo,
                    'total': total_bookings,
                    'percentage': (bookings_with_odoo / total_bookings * 100) if total_bookings > 0 else 0
                }
            }
        
        except Exception as e:
            logger.error(f"Error getting sync status: {str(e)}")
            return {'success': False, 'error': str(e)}

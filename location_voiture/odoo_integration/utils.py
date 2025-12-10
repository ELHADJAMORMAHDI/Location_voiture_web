"""
Utility functions for Odoo integration

This module provides helper functions for common Odoo operations.
"""

import logging
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)


def convert_car_to_odoo_format(django_car):
    """
    Convert Django Car model to Odoo fleet.vehicle format.
    
    Args:
        django_car: Car model instance
        
    Returns:
        dict: Data in Odoo format
    """
    return {
        'name': f"{django_car.year} {django_car.make} {django_car.model}",
        'license_plate': django_car.registration_number,
        'model_id': f"{django_car.make} {django_car.model}",
        'acquisition_date': f"{django_car.year}-01-01",
        'daily_rate': float(django_car.daily_rate),
        'seats': django_car.seats,
        'fuel_type': django_car.get_fuel_type_display(),
        'transmission': django_car.get_transmission_display(),
        'color': django_car.color,
    }


def convert_booking_to_odoo_format(django_booking):
    """
    Convert Django Booking to Odoo rental order format.
    
    Args:
        django_booking: Booking model instance
        
    Returns:
        dict: Data in Odoo format
    """
    return {
        'vehicle_id': django_booking.car.odoo_id,
        'customer_id': django_booking.customer.odoo_id,
        'start_date': django_booking.start_date.isoformat(),
        'end_date': django_booking.end_date.isoformat(),
        'pickup_location': django_booking.pickup_location,
        'return_location': django_booking.return_location,
        'daily_rate': float(django_booking.daily_rate),
        'number_of_days': django_booking.number_of_days,
        'total_cost': float(django_booking.total_cost),
        'state': 'draft',
        'notes': django_booking.notes,
    }


def calculate_rental_days(start_date, end_date):
    """
    Calculate number of days between two dates.
    
    Args:
        start_date: Start datetime
        end_date: End datetime
        
    Returns:
        int: Number of days
    """
    delta = end_date - start_date
    days = delta.days
    return days if days > 0 else 1


def calculate_total_cost(daily_rate, number_of_days, insurance=Decimal('0'), additional=Decimal('0')):
    """
    Calculate total rental cost.
    
    Args:
        daily_rate: Daily rental rate
        number_of_days: Number of days
        insurance: Insurance cost
        additional: Additional charges
        
    Returns:
        Decimal: Total cost
    """
    if isinstance(daily_rate, (int, float)):
        daily_rate = Decimal(str(daily_rate))
    
    subtotal = daily_rate * Decimal(number_of_days)
    total = subtotal + insurance + additional
    return total


def format_currency(amount):
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted currency
    """
    if isinstance(amount, Decimal):
        return f"${amount:.2f}"
    return f"${float(amount):.2f}"


def is_license_valid(license_expiry):
    """
    Check if driver's license is still valid.
    
    Args:
        license_expiry: Expiry date
        
    Returns:
        bool: True if valid, False if expired
    """
    from django.utils import timezone
    return license_expiry >= timezone.now().date()


def parse_odoo_date(odoo_date_str):
    """
    Parse Odoo date string to Python datetime.
    
    Args:
        odoo_date_str: Date string from Odoo (YYYY-MM-DD format)
        
    Returns:
        datetime: Parsed datetime
    """
    try:
        return datetime.strptime(odoo_date_str, '%Y-%m-%d')
    except ValueError:
        logger.error(f"Could not parse Odoo date: {odoo_date_str}")
        return None

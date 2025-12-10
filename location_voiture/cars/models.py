from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Car(models.Model):
    """Car model for rental service."""
    FUEL_CHOICES = [
        ('DIESEL', 'Diesel'),
        ('GASOLINE', 'Gasoline'),
        ('HYBRID', 'Hybrid'),
        ('ELECTRIC', 'Electric'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('MANUAL', 'Manual'),
        ('AUTOMATIC', 'Automatic'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('RENTED', 'Rented'),
        ('MAINTENANCE', 'Maintenance'),
        ('RESERVED', 'Reserved'),
    ]

    # Basic Information
    registration_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=100)  # Brand (e.g., Toyota)
    model = models.CharField(max_length=100)  # Model (e.g., Camry)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    
    # Features
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    mileage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Rental Information
    daily_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    # Image and Description
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    description = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True)  # e.g., ['GPS', 'AC', 'Bluetooth']
    
    # Metadata
    odoo_id = models.IntegerField(null=True, blank=True)  # Link to Odoo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Cars'
        indexes = [
            models.Index(fields=['status', 'daily_rate']),
            models.Index(fields=['make', 'model']),
        ]

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.registration_number})"

    def is_available(self):
        """Check if car is available for booking."""
        return self.status == 'AVAILABLE'


class Availability(models.Model):
    """Track car availability for specific dates."""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(db_index=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('car', 'date')
        verbose_name_plural = 'Availabilities'
        indexes = [
            models.Index(fields=['date', 'is_available']),
        ]

    def __str__(self):
        return f"{self.car} - {self.date}: {'Available' if self.is_available else 'Booked'}"


class Customer(models.Model):
    """Customer/User profile for rental system."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # License Information
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    
    # Rental History
    total_rentals = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    odoo_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Booking(models.Model):
    """Booking/Reservation model."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
        ('REFUNDED', 'Refunded'),
    ]

    # Reference
    booking_reference = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Customer & Car
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='bookings')
    
    # Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    return_location = models.CharField(max_length=255)
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_days = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    
    # Additional Information
    notes = models.TextField(blank=True)
    special_requests = models.TextField(blank=True)
    
    # Metadata
    odoo_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['car', 'start_date']),
            models.Index(fields=['status', 'payment_status']),
        ]

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.customer}"

    def calculate_cost(self):
        """Calculate total booking cost."""
        from datetime import datetime
        days = (self.end_date - self.start_date).days
        if days < 1:
            days = 1
        
        self.number_of_days = days
        self.subtotal = self.daily_rate * Decimal(days)
        self.total_cost = self.subtotal + self.insurance_cost + self.additional_charges
        return self.total_cost

    def is_active(self):
        """Check if booking is currently active."""
        return self.status == 'ACTIVE'

    def can_be_cancelled(self):
        """Check if booking can be cancelled."""
        return self.status in ['PENDING', 'CONFIRMED']

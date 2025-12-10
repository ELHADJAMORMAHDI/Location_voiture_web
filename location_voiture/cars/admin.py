from django.contrib import admin
from .models import Car, Availability, Customer, Booking


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'make', 'model', 'year', 'daily_rate', 'status']
    list_filter = ['status', 'fuel_type', 'transmission', 'year']
    search_fields = ['registration_number', 'make', 'model']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('registration_number', 'make', 'model', 'year')
        }),
        ('Features', {
            'fields': ('color', 'fuel_type', 'transmission', 'seats', 'mileage')
        }),
        ('Rental Information', {
            'fields': ('daily_rate', 'status')
        }),
        ('Details', {
            'fields': ('description', 'features', 'image')
        }),
        ('Odoo Integration', {
            'fields': ('odoo_id',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'is_available']
    list_filter = ['is_available', 'date']
    search_fields = ['car__registration_number']
    date_hierarchy = 'date'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone_number', 'city', 'total_rentals', 'is_verified']
    list_filter = ['is_verified', 'country']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    readonly_fields = ['created_at', 'updated_at', 'total_rentals', 'total_spent']
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city', 'postal_code', 'country')
        }),
        ('License Information', {
            'fields': ('license_number', 'license_expiry')
        }),
        ('Rental History', {
            'fields': ('total_rentals', 'total_spent')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_date')
        }),
        ('Odoo Integration', {
            'fields': ('odoo_id',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'customer', 'car', 'start_date', 'status', 'payment_status', 'total_cost']
    list_filter = ['status', 'payment_status', 'start_date', 'created_at']
    search_fields = ['booking_reference', 'customer__user__first_name', 'car__registration_number']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at', 'confirmed_at', 'completed_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference',)
        }),
        ('Customer & Car', {
            'fields': ('customer', 'car')
        }),
        ('Dates & Locations', {
            'fields': ('start_date', 'end_date', 'pickup_location', 'return_location')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'number_of_days', 'subtotal', 'insurance_cost', 'additional_charges', 'total_cost')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'special_requests')
        }),
        ('Odoo Integration', {
            'fields': ('odoo_id',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirm_booking', 'cancel_booking']

    def confirm_booking(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='PENDING').update(
            status='CONFIRMED',
            confirmed_at=timezone.now()
        )
        self.message_user(request, f'{updated} booking(s) confirmed.')
    confirm_booking.short_description = 'Confirm selected bookings'

    def cancel_booking(self, request, queryset):
        updated = queryset.filter(status__in=['PENDING', 'CONFIRMED']).update(status='CANCELLED')
        self.message_user(request, f'{updated} booking(s) cancelled.')
    cancel_booking.short_description = 'Cancel selected bookings'

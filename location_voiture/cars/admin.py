from django.contrib import admin
from .models import Car, Booking


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_day', 'available']
    list_filter = ['available']
    search_fields = ['name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'car', 'start_date', 'end_date']
    search_fields = ['customer_name']


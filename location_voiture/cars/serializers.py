from rest_framework import serializers
from .models import Car, Booking, Availability, Customer


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model."""
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'id', 'registration_number', 'make', 'model', 'year',
            'color', 'fuel_type', 'transmission', 'seats', 'mileage',
            'daily_rate', 'status', 'image', 'description', 'features',
            'is_available', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_is_available(self, obj):
        return obj.is_available()


class AvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for Availability model."""
    car_details = CarSerializer(source='car', read_only=True)
    
    class Meta:
        model = Availability
        fields = ['id', 'car', 'car_details', 'date', 'is_available']


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'user_email', 'user_name', 'phone_number',
            'address', 'city', 'postal_code', 'country',
            'license_number', 'license_expiry', 'total_rentals',
            'total_spent', 'is_verified'
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    car_details = CarSerializer(source='car', read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'customer', 'customer_details',
            'car', 'car_details', 'start_date', 'end_date',
            'pickup_location', 'return_location', 'daily_rate',
            'number_of_days', 'subtotal', 'insurance_cost',
            'additional_charges', 'total_cost', 'status',
            'payment_status', 'notes', 'special_requests',
            'created_at', 'confirmed_at', 'completed_at'
        ]
        read_only_fields = [
            'booking_reference', 'daily_rate', 'number_of_days',
            'subtotal', 'total_cost', 'created_at', 'confirmed_at',
            'completed_at'
        ]
        extra_kwargs = {
            'customer': {'write_only': True}
        }

    def validate(self, data):
        """Validate booking dates and car availability."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        car = data.get('car')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError("End date must be after start date.")
        
        # Check car availability
        if car and start_date and end_date:
            conflicting_bookings = Booking.objects.filter(
                car=car,
                start_date__lt=end_date,
                end_date__gt=start_date,
                status__in=['CONFIRMED', 'ACTIVE']
            )
            
            if conflicting_bookings.exists():
                raise serializers.ValidationError("Car is not available for the selected dates.")
        
        return data

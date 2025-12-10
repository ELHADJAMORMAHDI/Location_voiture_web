from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Car, Booking, Availability
from .serializers import CarSerializer, BookingSerializer, AvailabilitySerializer


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for cars.
    GET /api/cars/ - List all available cars
    GET /api/cars/{id}/ - Get car details
    """
    queryset = Car.objects.filter(status='AVAILABLE')
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fuel_type', 'transmission', 'seats']
    search_fields = ['make', 'model', 'registration_number']
    ordering_fields = ['daily_rate', 'created_at', 'year']

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability information for a specific car."""
        car = self.get_object()
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        today = timezone.now().date()
        future_date = today + timedelta(days=30)
        
        availabilities = Availability.objects.filter(
            car=car,
            date__range=[today, future_date],
            is_available=True
        ).values_list('date', flat=True)
        
        return Response({
            'car_id': car.id,
            'available_dates': list(availabilities)
        })


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings.
    POST /api/bookings/ - Create a new booking
    GET /api/bookings/ - List user's bookings
    PATCH /api/bookings/{id}/ - Update booking
    DELETE /api/bookings/{id}/ - Cancel booking
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the current user's bookings."""
        user = self.request.user
        try:
            customer = user.customer_profile
            return customer.bookings.all()
        except:
            return Booking.objects.none()

    def perform_create(self, serializer):
        """Create booking for current user."""
        import uuid
        from django.utils import timezone
        from decimal import Decimal
        
        user = self.request.user
        try:
            customer = user.customer_profile
        except:
            return Response(
                {'error': 'Customer profile not found. Please complete your profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create booking reference
        booking_reference = f"BK{uuid.uuid4().hex[:8].upper()}"
        
        # Get car and calculate cost
        car = serializer.validated_data['car']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        days = (end_date - start_date).days
        if days < 1:
            days = 1
        
        subtotal = car.daily_rate * Decimal(days)
        total_cost = subtotal + serializer.validated_data.get('insurance_cost', Decimal('0'))
        
        booking = serializer.save(
            customer=customer,
            booking_reference=booking_reference,
            daily_rate=car.daily_rate,
            number_of_days=days,
            subtotal=subtotal,
            total_cost=total_cost,
            status='PENDING'
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()
        
        if booking.can_be_cancelled():
            booking.status = 'CANCELLED'
            booking.save()
            return Response({'status': 'booking cancelled'})
        
        return Response(
            {'error': 'Booking cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a pending booking (Admin only)."""
        from django.utils import timezone
        
        booking = self.get_object()
        
        if booking.status == 'PENDING':
            booking.status = 'CONFIRMED'
            booking.confirmed_at = timezone.now()
            booking.save()
            return Response({'status': 'booking confirmed'})
        
        return Response(
            {'error': 'Only pending bookings can be confirmed'},
            status=status.HTTP_400_BAD_REQUEST
        )

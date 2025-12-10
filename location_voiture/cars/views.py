from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

from .models import Car, Booking, Availability, Customer
from .forms import BookingForm, CustomerProfileForm


def home(request):
    """Home page view."""
    featured_cars = Car.objects.filter(status='AVAILABLE')[:6]
    total_cars = Car.objects.filter(status='AVAILABLE').count()
    total_bookings = Booking.objects.filter(status='COMPLETED').count()
    
    context = {
        'featured_cars': featured_cars,
        'total_cars': total_cars,
        'total_bookings': total_bookings,
    }
    return render(request, 'cars/home.html', context)


class CarListView(ListView):
    """List all available cars."""
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        queryset = Car.objects.filter(status='AVAILABLE')
        
        # Filter by search query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(make__icontains=query) |
                Q(model__icontains=query) |
                Q(registration_number__icontains=query)
            )
        
        # Filter by fuel type
        fuel = self.request.GET.get('fuel')
        if fuel:
            queryset = queryset.filter(fuel_type=fuel)
        
        # Filter by transmission
        transmission = self.request.GET.get('transmission')
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(daily_rate__gte=min_price)
        if max_price:
            queryset = queryset.filter(daily_rate__lte=max_price)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fuel_choices'] = Car.FUEL_CHOICES
        context['transmission_choices'] = Car.TRANSMISSION_CHOICES
        return context


class CarDetailView(DetailView):
    """Car detail page."""
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get available dates for the next 30 days
        car = self.get_object()
        today = timezone.now().date()
        future_date = today + timedelta(days=30)
        
        availabilities = Availability.objects.filter(
            car=car,
            date__range=[today, future_date]
        ).values_list('date', 'is_available')
        
        context['available_dates'] = dict(availabilities)
        return context


class BookingCreateView(LoginRequiredMixin, CreateView):
    """Create a new booking."""
    model = Booking
    form_class = BookingForm
    template_name = 'cars/booking_form.html'
    success_url = reverse_lazy('cars:booking_confirmation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get car if provided
        car_id = self.request.GET.get('car')
        if car_id:
            context['car'] = get_object_or_404(Car, id=car_id)
        
        return context

    def form_valid(self, form):
        """Process valid form."""
        booking = form.save(commit=False)
        
        # Get or create customer profile
        try:
            customer = self.request.user.customer_profile
        except Customer.DoesNotExist:
            return redirect('accounts:profile_setup')
        
        booking.customer = customer
        booking.daily_rate = booking.car.daily_rate
        booking.booking_reference = f"BK{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate costs
        booking.calculate_cost()
        booking.save()
        
        return super().form_valid(form)


@login_required
def booking_confirmation(request, pk=None):
    """Booking confirmation page."""
    try:
        customer = request.user.customer_profile
        booking = customer.bookings.latest('created_at')
    except (Customer.DoesNotExist, Booking.DoesNotExist):
        return redirect('home')
    
    context = {'booking': booking}
    return render(request, 'cars/booking_confirmation.html', context)


@login_required
def my_bookings(request):
    """View user's bookings."""
    try:
        customer = request.user.customer_profile
        bookings = customer.bookings.all()
    except Customer.DoesNotExist:
        return redirect('accounts:profile_setup')
    
    context = {'bookings': bookings}
    return render(request, 'cars/my_bookings.html', context)


@login_required
def cancel_booking(request, pk):
    """Cancel a booking."""
    try:
        customer = request.user.customer_profile
        booking = customer.bookings.get(id=pk)
    except (Customer.DoesNotExist, Booking.DoesNotExist):
        return redirect('home')
    
    if booking.can_be_cancelled():
        booking.status = 'CANCELLED'
        booking.save()
    
    return redirect('cars:my_bookings')


@login_required
def dashboard(request):
    """Customer dashboard."""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return redirect('accounts:profile_setup')
    
    active_bookings = customer.bookings.filter(status__in=['ACTIVE', 'CONFIRMED'])
    completed_bookings = customer.bookings.filter(status='COMPLETED')
    
    context = {
        'customer': customer,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
    }
    return render(request, 'cars/dashboard.html', context)

from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('booking/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

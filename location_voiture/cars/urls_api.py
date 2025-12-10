from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import CarViewSet, BookingViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]

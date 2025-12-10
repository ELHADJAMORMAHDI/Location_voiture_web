from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.car_list, name='car_list'),  # قائمة السيارات
    path('<int:pk>/', views.car_detail, name='car_detail'),  # تفاصيل السيارة
    path('<int:pk>/book/', views.book_car, name='book_car'),  # حجز السيارة
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),  # تأكيد الحجز
    path('my-bookings/', views.my_bookings, name='my_bookings'),  # حجوزاتي
]

"""
اختبارات بسيطة للتحقق من المشروع
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_voiture.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from cars.models import Car, Booking
from datetime import date

class CarModelTest(TestCase):
    """اختبار نموذج السيارة"""
    
    def setUp(self):
        Car.objects.create(
            name='تويوتا',
            price_per_day=5000,
            description='سيارة جيدة',
            available=True
        )
    
    def test_car_creation(self):
        """اختبار إنشاء سيارة"""
        car = Car.objects.get(name='تويوتا')
        self.assertEqual(car.price_per_day, 5000)
        self.assertTrue(car.available)
    
    def test_car_str(self):
        """اختبار طريقة __str__ للسيارة"""
        car = Car.objects.get(name='تويوتا')
        self.assertEqual(str(car), 'تويوتا')


class BookingModelTest(TestCase):
    """اختبار نموذج الحجز"""
    
    def setUp(self):
        self.car = Car.objects.create(
            name='هونداي',
            price_per_day=4000,
            description='سيارة اقتصادية'
        )
        
        Booking.objects.create(
            customer_name='أحمد',
            car=self.car,
            start_date=date(2025, 12, 15),
            end_date=date(2025, 12, 20),
            total_price=20000
        )
    
    def test_booking_creation(self):
        """اختبار إنشاء حجز"""
        booking = Booking.objects.get(customer_name='أحمد')
        self.assertEqual(booking.total_price, 20000)
        self.assertEqual(booking.car.name, 'هونداي')


class ViewsTest(TestCase):
    """اختبار العروض (Views)"""
    
    def setUp(self):
        self.client = Client()
        self.car = Car.objects.create(
            name='مرسيدس',
            price_per_day=8000,
            description='سيارة فاخرة'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_home_view(self):
        """اختبار الصفحة الرئيسية"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_car_list_view(self):
        """اختبار قائمة السيارات"""
        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'مرسيدس')
    
    def test_car_detail_view(self):
        """اختبار تفاصيل السيارة"""
        response = self.client.get(f'/cars/{self.car.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'مرسيدس')


if __name__ == '__main__':
    print("✅ تم تشغيل الاختبارات!")

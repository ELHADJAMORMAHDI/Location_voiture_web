import os
import sys
import django

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'location_voiture.settings')
django.setup()

from django.contrib.auth.models import User
from cars.models import Car

# إنشاء حساب المسؤول إذا لم يكن موجوداً
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'password123')
    print("✅ تم إنشاء حساب المسؤول - admin / password123")
else:
    print("⚠️  حساب المسؤول موجود بالفعل")

# إضافة بعض السيارات التجريبية
cars_data = [
    {
        'name': 'تويوتا كامري',
        'price_per_day': 5000,
        'description': 'سيارة حديثة وموثوقة',
        'available': True
    },
    {
        'name': 'هونداي أكورد',
        'price_per_day': 4500,
        'description': 'سيارة مريحة وآقتصادية',
        'available': True
    },
    {
        'name': 'مرسيدس بنز',
        'price_per_day': 8000,
        'description': 'سيارة فاخرة وراقية',
        'available': True
    },
    {
        'name': 'بيجو 2008',
        'price_per_day': 3500,
        'description': 'سيارة اقتصادية وآمنة',
        'available': True
    },
]

for car_data in cars_data:
    if not Car.objects.filter(name=car_data['name']).exists():
        Car.objects.create(**car_data)
        print(f"✅ تم إضافة السيارة: {car_data['name']}")
    else:
        print(f"⚠️  السيارة {car_data['name']} موجودة بالفعل")

print("\n✅ تم إنشاء البيانات بنجاح!")

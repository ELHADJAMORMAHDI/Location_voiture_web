from django.db import models


# 🚗 نموذج السيارة - بسيط جداً
class Car(models.Model):
    name = models.CharField(max_length=100)  # اسم السيارة (مثلاً: تويوتا كامري)
    price_per_day = models.IntegerField()  # السعر في اليوم
    image = models.ImageField(upload_to='cars/', null=True, blank=True)  # صورة السيارة
    description = models.TextField()  # وصف قصير
    available = models.BooleanField(default=True)  # هل السيارة متاحة؟
    
    def __str__(self):
        return self.name


# 📅 نموذج الحجز - بسيط جداً
class Booking(models.Model):
    customer_name = models.CharField(max_length=100)  # اسم الزبون
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # السيارة المحجوزة
    start_date = models.DateField()  # تاريخ البداية
    end_date = models.DateField()  # تاريخ النهاية
    total_price = models.IntegerField(default=0)  # السعر النهائي
    created_at = models.DateTimeField(auto_now_add=True)  # التاريخ
    
    def __str__(self):
        return f"{self.customer_name} - {self.car.name}"

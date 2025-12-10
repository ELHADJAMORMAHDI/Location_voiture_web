from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, Booking


# 🏠 الصفحة الرئيسية
def home(request):
    cars = Car.objects.all()[:6]  # عرض أول 6 سيارات
    return render(request, 'cars/home.html', {'cars': cars})


# 🚗 قائمة جميع السيارات
def car_list(request):
    cars = Car.objects.all()  # جميع السيارات
    return render(request, 'cars/car_list.html', {'cars': cars})


# 📋 تفاصيل السيارة
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})


# 📅 نموذج الحجز (للعضو المسجل فقط)
@login_required
def book_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        # الحصول على البيانات من النموذج
        customer_name = request.POST.get('customer_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # حساب عدد الأيام والسعر
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        days = (end - start).days
        total_price = days * car.price_per_day
        
        # حفظ الحجز
        booking = Booking.objects.create(
            customer_name=customer_name,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        
        return redirect('booking_confirmation', booking_id=booking.id)
    
    return render(request, 'cars/booking_form.html', {'car': car})


# ✅ تأكيد الحجز
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'cars/booking_confirmation.html', {'booking': booking})


# 👤 حجوزاتي
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer_name=request.user.username)
    return render(request, 'cars/my_bookings.html', {'bookings': bookings})

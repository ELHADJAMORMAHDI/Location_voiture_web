@echo off
REM =====================================================
REM تشغيل مشروع Location Voiture البسيط - Windows
REM =====================================================

color 0A
echo.
echo 🚗 مشروع تأجير السيارات - Location Voiture
echo ========================================
echo.

REM تنشيط البيئة الافتراضية
echo 📦 تنشيط البيئة الافتراضية...
call .venv\Scripts\activate.bat

REM الذهاب للمجلد الرئيسي
cd location_voiture

REM التحقق من قاعدة البيانات
echo ✅ التحقق من قاعدة البيانات...
python manage.py migrate

REM تشغيل الخادم
echo.
echo 🚀 تشغيل الخادم...
echo 📍 اذهب إلى: http://127.0.0.1:8000/
echo 👨‍💼 المسؤول: http://127.0.0.1:8000/admin/
echo    Username: admin
echo    Password: password123
echo.

python manage.py runserver

pause

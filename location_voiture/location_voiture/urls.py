"""
Routing URLs - مسارات الويب
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars import views as cars_views

urlpatterns = [
    path('admin/', admin.site.urls),  # لوحة التحكم
    path('', cars_views.home, name='home'),  # الصفحة الرئيسية
    path('cars/', include('cars.urls')),  # تطبيق السيارات
    path('accounts/', include('accounts.urls')),  # تطبيق الحسابات
]

# عرض الصور والملفات المرفوعة
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

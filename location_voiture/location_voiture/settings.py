"""
Django settings for location_voiture project - مشروع تأجير السيارات
إعدادات بسيطة للمبتدئين
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔑 مفتاح سري (غيره لاحقاً في الإنتاج!)
SECRET_KEY = 'django-insecure-change-this-in-production'

# 🔴 DEBUG = True (فقط في التطوير)
DEBUG = True

ALLOWED_HOSTS = ['*']

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # تطبيقاتنا
    'cars.apps.CarsConfig',
    'accounts.apps.AccountsConfig',
]

# البرامج الوسيطة (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'location_voiture.urls'

# القوالب (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'location_voiture.wsgi.application'

# 📊 قاعدة البيانات (SQLite - بسيطة!)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# التدويل (Internationalization)
LANGUAGE_CODE = 'ar'  # اللغة العربية
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_TZ = True

# الملفات الثابتة (CSS, JS, صور)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ملفات الوسائط (الصور المرفوعة)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# نوع المفتاح الأساسي الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# تسجيل الدخول
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

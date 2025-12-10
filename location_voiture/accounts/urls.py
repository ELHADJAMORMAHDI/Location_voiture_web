from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # تسجيل حساب
    path('login/', views.login_view, name='login'),  # تسجيل دخول
    path('logout/', views.logout_view, name='logout'),  # تسجيل خروج
    path('profile/', views.profile, name='profile'),  # الملف الشخصي
]

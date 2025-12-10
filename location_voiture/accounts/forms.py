from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# 📝 نموذج التسجيل البسيط
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# 🔑 نموذج تسجيل الدخول
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

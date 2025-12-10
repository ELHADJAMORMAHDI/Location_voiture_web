from django import forms
from .models import Booking, Customer


class BookingForm(forms.ModelForm):
    """Form for creating/updating bookings."""
    
    class Meta:
        model = Booking
        fields = ['car', 'start_date', 'end_date', 'pickup_location', 'return_location', 'special_requests']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Airport Terminal 1'}),
            'return_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Downtown Office'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data


class CustomerProfileForm(forms.ModelForm):
    """Form for customer profile information."""
    
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'city', 'postal_code', 'country', 'license_number', 'license_expiry']
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

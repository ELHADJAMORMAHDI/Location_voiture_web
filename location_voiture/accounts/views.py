from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, LoginForm
from cars.models import Customer
from cars.forms import CustomerProfileForm


def signup(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile_setup')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('home')


@login_required
def profile_setup(request):
    """Complete customer profile setup."""
    try:
        customer = request.user.customer_profile
        return redirect('cars:dashboard')
    except Customer.DoesNotExist:
        if request.method == 'POST':
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()
                return redirect('cars:dashboard')
        else:
            form = CustomerProfileForm()
        
        context = {'form': form, 'step': 'setup'}
        return render(request, 'accounts/profile_setup.html', context)


@login_required
def profile_edit(request):
    """Edit customer profile."""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return redirect('accounts:profile_setup')
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('cars:dashboard')
    else:
        form = CustomerProfileForm(instance=customer)
    
    context = {'form': form, 'step': 'edit'}
    return render(request, 'accounts/profile_setup.html', context)


@login_required
def profile_view(request):
    """View customer profile."""
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return redirect('accounts:profile_setup')
    
    context = {'customer': customer}
    return render(request, 'accounts/profile.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DonorRegistrationForm, FoodbankRegistrationForm, RecipientRegistrationForm, LoginForm
from .models import User #, Donor, Foodbank, Recipient # Potentially needed for dashboards

# Registration Views
def donor_register_view(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('AuthApp:donor_dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = DonorRegistrationForm()
    return render(request, 'AuthApp/donor_register.html', {'form': form})

def foodbank_register_view(request):
    if request.method == 'POST':
        form = FoodbankRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('AuthApp:foodbank_dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = FoodbankRegistrationForm()
    return render(request, 'AuthApp/foodbank_register.html', {'form': form})

def recipient_register_view(request):
    if request.method == 'POST':
        form = RecipientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('AuthApp:recipient_dashboard')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RecipientRegistrationForm()
    return render(request, 'AuthApp/recipient_register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username') # AuthenticationForm uses 'username'
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.email}.")
                if user.user_type == 'DONOR':
                    return redirect('AuthApp:donor_dashboard')
                elif user.user_type == 'FOODBANK':
                    return redirect('AuthApp:foodbank_dashboard')
                elif user.user_type == 'RECIPIENT':
                    return redirect('AuthApp:recipient_dashboard')
                else:
                    # Fallback, though user_type should always be set
                    messages.error(request, "User type not recognized.")
                    return redirect('AuthApp:login') # Or a generic home page
            else:
                messages.error(request, "Invalid email or password.")
        else:
            # Form is not valid (e.g. email format incorrect)
            messages.error(request, "Invalid form submission. Please check your email and password.")
    else:
        form = LoginForm()
    return render(request, 'AuthApp/login.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('AuthApp:login')

# Dashboard Views (Placeholders)
@login_required
def donor_dashboard_view(request):
    if request.user.user_type != 'DONOR':
        messages.error(request, "Access Denied.")
        return redirect('AuthApp:login') # Or a generic error page/home
    # donor_profile = Donor.objects.get(user=request.user) # Example if you need donor specific data
    return render(request, 'AuthApp/donor_dashboard.html', {'user': request.user})

@login_required
def foodbank_dashboard_view(request):
    if request.user.user_type != 'FOODBANK':
        messages.error(request, "Access Denied.")
        return redirect('AuthApp:login')
    # foodbank_profile = Foodbank.objects.get(user=request.user) # Example
    return render(request, 'AuthApp/foodbank_dashboard.html', {'user': request.user})

@login_required
def recipient_dashboard_view(request):
    if request.user.user_type != 'RECIPIENT':
        messages.error(request, "Access Denied.")
        return redirect('AuthApp:login')
    # recipient_profile = Recipient.objects.get(user=request.user) # Example
    return render(request, 'AuthApp/recipient_dashboard.html', {'user': request.user})

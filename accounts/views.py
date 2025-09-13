from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import re
# Create your views here.

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'home.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        user = authenticate(request, username=user_or_email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    # Always render the login page (even if it's a GET or failed POST)
    return render(request, 'login.html')

@never_cache
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Split full name into first and last
        name_parts = full_name.strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Username from email before @
        username = email.split('@')[0]

        # --------- Validation ---------

        # Email Pattern
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email format.")
            return render(request, 'registration.html')

        # Password Length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'registration.html')

        # Passwords match?
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration.html')

        # check user exist or not
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration.html')

        # check emil register or not
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        # 👇 THIS LINE IS IMPORTANT
        user.backend = 'accounts.backend.EmailOrUsernameModelBackend'

        login(request, user)  # Auto login after register
        return redirect('home')  # Or your dashboard URL

    return render(request, 'registration.html')


def logout_view(request):
    logout(request)  # Destroys the user session
    return redirect('login')  # Redirect to login page (or any other)


def reset_username_email_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username_or_email')
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                user = None

        if user:
            return redirect('reset_step2', username=user.username)
        else:
            messages.error(request, "User not found with that username or email.")

    return render(request, 'reset_username.html')


def reset_password_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 6:
            messages.error(request, "Password should be at least 6 characters.")
        else:
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect('login')

    return render(request, 'reset_password.html', {'username': username})


@login_required
def profile_view(request):
    user = request.user

    # Get or create profile if missing
    profile, created = Profile.objects.get_or_create(user=user)


    if request.method == 'POST':
        new_username = request.POST.get('username').strip()
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        if new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists.")
                return redirect('profile')
            else:
                user.username = new_username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if phone:
            profile.phone = phone


        user.save()
        profile.save()

        messages.success(request, "Profile updated.")
        return redirect('profile')  # After saving, redirect to same page

    return render(request, 'profile.html', {'user': user, 'profile': profile})

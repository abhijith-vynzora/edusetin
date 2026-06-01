from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentLoginForm
from .models import Student

def student_register(request):
    if request.user.is_authenticated:
        return redirect('student_portal:dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Create Django User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Create Student Profile
            Student.objects.create(
                user=user,
                full_name=full_name
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, "Registration successful! Welcome to your dashboard.")
            return redirect('student_portal:dashboard')
    else:
        form = StudentRegistrationForm()
        
    return render(request, 'student_portal/register.html', {'form': form})

def student_login(request):
    if request.user.is_authenticated:
        return redirect('student_portal:dashboard')

    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_portal:dashboard')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = StudentLoginForm()

    return render(request, 'student_portal/login.html', {'form': form})

@login_required(login_url='student_portal:login')
def student_dashboard(request):
    # Try to get the student profile, fallback if admin or staff logs in directly
    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student
        
    return render(request, 'student_portal/dashboard.html', {'student': student})

def student_logout(request):
    logout(request)
    return redirect('student_portal:login')

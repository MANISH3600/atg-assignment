from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from .models import UserProfile
from django.core.exceptions import PermissionDenied
from .forms import CustomLoginForm
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from .models import UserProfile

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            elif user.user_type == 'doctor':
                return redirect('doctor_dashboard')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
            else:
                return HttpResponse("Invalid username or password.")
        else:
            return HttpResponse("Invalid form data.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})
def patient_dashboard(request):
    if (request.user.user_type) != "patient":
        return HttpResponse('you dont have permission to access this page')
    return render(request, 'accounts/patient_dashboard.html')

def doctor_dashboard(request):
    if (request.user.user_type) != "doctor":
        return HttpResponse('you dont have permission to access this page')
    return render(request, 'accounts/doctor_dashboard.html')

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


def index(request):
    return render(request, 'accounts/dashboard.html')
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





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def create_blog_post(request):
    if request.user.user_type != 'doctor':
        return HttpResponse("not allowed")
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('my_posts')
    else:
        form = BlogPostForm()
    return render(request, 'accounts/create_blog_post.html', {'form': form})

@login_required
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'accounts/my_posts.html', {'posts': posts})

CATEGORY_MAPPING = {
    'Mental Health': 'MH',
    'Heart Disease': 'HD',
    'Covid19': 'CV',
    'Immunization': 'IM',
}

def view_blog_posts(request):
    category_name = request.GET.get('category')
    category_code = CATEGORY_MAPPING.get(category_name)
    
    if category_code:
        posts = BlogPost.objects.filter(category=category_code, is_draft=False)
    else:
        posts = BlogPost.objects.filter(is_draft=False)
    
    return render(request, 'accounts/view_blog_posts.html', {'posts': posts})

def view_blog_category(request, category):
    print(category)
    posts = BlogPost.objects.filter(category=category, is_draft=False)
    print(posts)
    return render(request, 'accounts/view_blog_category.html', {'posts': posts, 'category': category})



@login_required
def blog_post_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk, is_draft=False)
    return render(request, 'accounts/blog_post_detail.html', {'blog_post': blog_post})
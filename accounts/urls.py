from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('posts/', views.view_blog_posts, name='view_blog_posts'),
    path('category/<str:category>/', views.view_blog_category, name='view_blog_category'),
    path('view_post/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
]

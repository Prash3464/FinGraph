from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('reset/', views.reset_username_email_view, name='reset_step1'),
    path('reset-password/<str:username>/', views.reset_password_view, name='reset_step2'),
    path('profile/', views.profile_view, name='profile'),
]
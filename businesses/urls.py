# businesses/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='businesses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='businesses/logout.html'), name='logout'),
]

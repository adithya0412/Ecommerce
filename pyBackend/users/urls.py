from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register', views.register, name='register_no_slash'),
    path('login/', views.login, name='login'),
    path('login', views.login, name='login_no_slash'),
    path('profile/', views.get_profile, name='get_profile'),
    path('profile', views.get_profile, name='get_profile_no_slash'),
]

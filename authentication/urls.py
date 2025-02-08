from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('google-login/', views.google_login_view, name='google-login'),
    #path('logout/', views.logout_view, name='logout'),
    #path('register/', views.register_view, name='register'),
    #path('profile/',views.profile_view, name='profile'),
]

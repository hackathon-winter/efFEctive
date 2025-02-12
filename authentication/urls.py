from django.urls import path
from authentication.auth_views import login_view, logout_view
from authentication.google_auth_views import google_login
from authentication.register_views import register_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('google-login/', google_login, name='google-login'),
    path('register/', register_view, name='register'),
]

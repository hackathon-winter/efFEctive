from django.urls import path
from authentication.auth_views import login_view, logout_view
from authentication.google_auth_views import google_login
from authentication.register_views import register_view
from authentication.google_register_views import google_register

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('google/callback/', google_login, name='google_callback'),
    path('google_login/', google_login, name='google_login'),
    path('register/', register_view, name='register'),
    path('google_register/', google_register, name='google_register'),
]
from django.urls import path
from authentication.views.auth import login_view, logout_view
from authentication.views.register import register_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

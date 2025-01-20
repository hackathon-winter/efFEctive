from django.urls import path
from . import views

urlpattern = [
    path('login./'), views.login_view, name='login'),
    path('logout/'), view.logout_view, name='logout'),
    path('register/'), view.register_view, name='register'),
    path('profile/'),view.profile_view, name='profile'),
]

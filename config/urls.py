from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from authentication.views import home_view

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', redirect_to_home),
    path('home/', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('questions/', include('questions.urls')),
    path('progress/', include('progress.urls')),
    path('rewards/', include('rewards.urls')), 
]
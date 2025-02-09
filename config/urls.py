from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('questions/', include('questions.urls')),
    path('progress/', include('progress.urls')),
    path('rewards/', include('rewards.urls')), 
]

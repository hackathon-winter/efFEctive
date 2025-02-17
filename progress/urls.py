from django.urls import path
from . import views

urlpatterns = [
    path('progress/', views.view_progress, name='learning_history'),
]

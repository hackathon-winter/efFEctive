from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_progress, name='view_progress'),
    # path('reset/', view.reset_progress), name='reset_progress'),
    # path('update/', view.update_progress, name='update_progress'),
]

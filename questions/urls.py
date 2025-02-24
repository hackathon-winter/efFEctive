from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.list_questions, name='list_questions'),
    path('questions/<int:question_id>/submit/', views.answer_save, name='answer_save'),
    path('questions/<int:question_id>/answer/', views.answer_result, name='answer_result'),
    path('continue/', views.continue_questions, name='continue_questions'),
    path('end_session/', views.end_session, name='end_session'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.list_questions, name='list_questions'),
    path('questions/<int:question_id>/answer/', views.answer_save, name='answer_result'),
    path('questions/submit/', views.answer_save, name='answer_save'),
    path('continue/', views.continue_questions, name='continue_questions'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.list_questions, name='list_questions'),
    path('questions/<int:question_id>/answer/', views.answer_save, name='answer_save'),
    #path('detail/<int:question_id>', views.question_detail, name='question_detail'),
    #path('submit/', views.submit_answer, name='submit_answer'),
]

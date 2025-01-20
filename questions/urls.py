from django.urls import path
from . import views

urlpattern = [
    path('list/', views.list_questions, name='list_questions'),
    path('detail/<int:question_id>', views.question_detail, name='question_detail'),
    path('submit/', views.submit_answer), name='submit_answer'),
]

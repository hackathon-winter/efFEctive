from django.contrib import admin
from .models import Question,Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_diaplay = ('id', 'content', 'difficulty', 'created_at', 'updated_at')
    list_filter =('difficulty', 'created_at')
    search_fields = ('content',)
    ordering = ('-created_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_diaplay = ('id', 'question', 'selected_answer', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('selected_answer',)
    ordering = ('-created_at',)
from django.contrib import admin
from .models import Session

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'correct_answers', 'total_questions', 'progress_percentage', 'start_time', 'end_time')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user__user_name', 'user__email', 'session_id')
    ordering = ('-created_at',)

admin.site.register(Session, SessionAdmin)
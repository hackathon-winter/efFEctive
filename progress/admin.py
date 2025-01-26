from django.contrib import admin
from .models import Session

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'correct_user', 'total_questions', 'progress_percentage', 'start_time', 'end_time')
    list_filter = ('user', 'create_at', 'update_at')
    search_fields = ('user__user_name', 'user__email', 'session_id')
    ordering = ('-created_at',)

admin.site.register(Session, SessionAdmin)
from django.contrib import admin
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'level', 'acquired_at')
    list_filter = ('category', 'level')
    search_fields = ('user__user_name', 'category')
    ordering = ('-acquired_at',)

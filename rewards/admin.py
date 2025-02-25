from django.contrib import admin
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('display_users', 'category', 'level', 'acquired_at')
    list_filter = ('category', 'level')
    search_fields = ('user__user_name', 'category')
    ordering = ('-acquired_at',)

    def display_users(self, obj):
        return ", ".join([user.email for user in obj.users.all()])
    display_users.short_description = '取得ユーザー'

from django.contrib import admin
from .models import Badge, BadgesAwarded

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('display_users', 'category', 'level')
    list_filter = ('category', 'level')
    search_fields = ('user__user_name', 'category')
    ordering = ('category', 'level')

    def display_users(self, obj):
        return ", ".join([user.email for user in obj.users.all()])
    display_users.short_description = '取得ユーザー'

@admin.register(BadgesAwarded)
class BadgesAwardedAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'acquired_at')
    list_filter = ('badge__category', 'badge__level')
    search_fields = ('user__user_name', 'badge__category')
    ordering = ('-acquired_at',)
from django.db import models
from authentication.models import User
from questions.models import Question

class Badge(models.Model):
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'

    BADGE_LEVELS = [
        (BRONZE, 'ブロンズ'),
        (SILVER, 'シルバー'),
        (GOLD, 'ゴールド'),
    ]

    category = models.CharField(max_length=50, choices=Question.CATEGORY_CHOICES, verbose_name='カテゴリ')
    level = models.CharField(max_length=10, choices=BADGE_LEVELS, verbose_name='ランク')

    def __str__(self):
        return f'{self.get_category_display()}({self.get_level_display()})'

class BadgesAwarded(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badge_awards')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='badge_users')
    acquired_at = models.DateTimeField(auto_now_add=True, verbose_name='獲得日時')

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f'{self.user.user_name} - {self.badge}'

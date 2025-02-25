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

    users = models.ManyToManyField(
        'authentication.User',
        blank=True,
        verbose_name='取得ユーザー',
        related_name='badges_awarded'
    )

    category = models.CharField(max_length=50, choices=Question.CATEGORY_CHOICES, verbose_name='カテゴリ')
    level = models.CharField(max_length=10, choices=BADGE_LEVELS, verbose_name='ランク')
    acquired_at = models.DateTimeField(auto_now_add=True, verbose_name='獲得日時')

    class Meta:
        unique_together = ('category', 'level')

    def __str__(self):
        return f'{self.get_category_display()}({self.get_level_display()})'

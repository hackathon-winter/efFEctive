from django.db import models
from django.utils.timezone import now
from authentication.models import User

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)  # セッションID（自動採番）
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='sessions', verbose_name='ユーザー')
    correct_answers = models.IntegerField(default=0, verbose_name='正答数')
    total_questions = models.IntegerField(default=0, verbose_name='総問題数')
    consecutive_correct = models.IntegerField(default=0, verbose_name='連続正解数')    
    score = models.IntegerField(default=0, verbose_name='スコア')
    session_answers = models.JSONField(default=list, verbose_name='解答履歴')
    session_times = models.JSONField(default=list, verbose_name='解答時間履歴')
    start_time = models.DateTimeField(null=True, verbose_name='セッション開始日時')
    end_time = models.DateTimeField(null=True, verbose_name='セッション終了日時')
    created_at = models.DateTimeField(default=now, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    DIFFICULTY_CHOICES = [
        ('normal', 'Normal'),
        ('hard', 'Hard'),
    ]
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='normal',
        verbose_name='現在の難易度',
    )
    previous_difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='normal',
        verbose_name='前回の難易度',
    )

    def progress_percentage(self):
        if self.total_questions > 0:
            return(self.correct_answers / self.total_questions)* 100
        return 0

    def __str__(self):
        return f'Session {self.session_id} - User {getattr(self.user, 'user_name', 'Unknown User')} - {self.difficulty}'

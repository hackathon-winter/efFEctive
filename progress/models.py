from django.db import models
from django.utils.timezone import now

# Create your models here.

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)  # セッションID（自動採番）
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="sessions", verbose_name="ユーザー")
    correct_answers = models.IntegerField(verbose_name="正答数")
    total_questions = models.IntegerField(verbose_name="総問題数")
    progress_percentage = models.FloatField(verbose_name="進捗率")
    start_time = models.DateTimeField(null=True, verbose_name="セッション開始日時")
    end_time = models.DateTimeField(null=True, verbose_name="セッション終了日時")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return f"Session {self.session_id} - User {self.user.user_name}"

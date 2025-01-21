from django.db import models
from django.utils.timezone import now

# Create your models here.

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)  # 問題ID（自動採番）
    content = models.TextField(verbose_name="問題の内容")
    genre = models.CharField(max_length=50, verbose_name="ジャンル")
    difficulty = models.CharField(max_length=20, choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], verbose_name="難易度")
    choices = models.JSONField(verbose_name="選択肢")
    correct_answer = models.CharField(max_length=255, verbose_name="正解の選択肢")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return self.content[:50]


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)  # 回答ID（自動採番）
    session = models.ForeignKey('progress.Session', on_delete=models.CASCADE, related_name="answers", verbose_name="セッション")
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name="answers", verbose_name="問題")
    user_answer = models.IntegerField(verbose_name="ユーザーの回答")
    is_correct = models.BooleanField(verbose_name="正解かどうか")
    created_at = models.DateTimeField(default=now, verbose_name="回答日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return f"Answer {self.answer_id} - Session {self.session.session_id}"

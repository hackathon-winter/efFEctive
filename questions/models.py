from django.db import models
from django.utils.timezone import now

# Create your models here.

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('normal', 'Normal'),
        ('hard', 'Hard'),
    ]

    content = models.TextField(verbose_name="問題文")
    choices = models.JSONField(verbose_name="選択肢（JSON形式）")
    correct_answer = models.CharField(max_length=255, verbose_name="正解")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name="難易度")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="問題作成日時")

    def __str__(self):
        return self.content[:50]  # 問題文の先頭50文字を表示

    class Meta:
        verbose_name = "問題"
        verbose_name_plural = "問題"


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)  # 回答ID（自動採番）
    session = models.ForeignKey('progress.Session', on_delete=models.CASCADE, verbose_name="セッション")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="問題ID")
    selected_answer = models.CharField(max_length=255, verbose_name="ユーザーの選択した回答")
    is_correct = models.BooleanField(verbose_name="正解かどうか")
    time_taken = models.FloatField(verbose_name="回答時間（秒）")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="解答日時")

    def __str__(self):
        return f"Answer {self.answer_id} - Session {self.session.session_id}"
        #return f"{self.progress.Session_id} - {self.question.content[:50]}"

    class Meta:
        verbose_name = "解答"
        verbose_name_plural = "解答"
from django.db import models
from django.utils.timezone import now
from authentication.models import User
from progress.models import Session

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('normal', 'Normal'),
        ('hard', 'Hard'),
    ]

    CATEGORY_CHOICES = [
        ('fundamental_theory', '基礎理論'),
        ('algorithm', 'アルゴリズムとプログラミング'),
        ('computer_system', 'コンピューターの構成要素'),
        ('system_software', 'システム構成要素'),
        ('software', 'ソフトウェア'),
        ('hardware', 'ハードウェア'),
        ('user_interface', 'ユーザーインターフェース'),
        ('database', 'データベース'),
        ('network', 'ネットワーク'),
        ('security', 'セキュリティ'),
        ('system_development', 'システム開発技術'),
        ('software_development', 'ソフトウェア開発技術'),
        ('management', 'マネジメント系'),
        ('strategy', 'ストラテジ系'),
    ]

    content = models.TextField(verbose_name='問題文')
    choices = models.JSONField(verbose_name='選択肢（JSON形式）')
    correct_answer = models.CharField(max_length=255, verbose_name='正解')
    explanation =models.TextField(null=True, blank=True, verbose_name='解説')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name='難易度', default ='normal')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fundamental_theory', verbose_name='カテゴリ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='問題作成日時')

    def __str__(self):
        return f'[{self.get_category_display()}] {self.content[:50]}'

    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)  # 回答ID（自動採番）
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='セッション')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='問題ID')
    selected_answer = models.CharField(max_length=255, verbose_name='ユーザーの選択した回答')
    is_correct = models.BooleanField(verbose_name='正解かどうか', default=False)
    awarded = models.BooleanField(default=False)
    time_taken = models.FloatField(verbose_name='回答時間（秒）')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='解答日時')

    def save(self, *args, **kwargs): # 計算の自動化
        if self.selected_answer and self.question:
            self.is_correct = self.selected_answer == self.question.correct_answer
        else:
            self.is_correct = False
        super().save( *args, **kwargs)

    def __str__(self):
        return f'Answer {self.answer_id} - Session {self.session.id}'

    class Meta:
        verbose_name = '解答'
        verbose_name_plural = '解答'
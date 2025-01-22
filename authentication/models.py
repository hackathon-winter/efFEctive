from django.db import models
from django.utils.timezone import now

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # ユーザーID（自動採番）
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    password_hash = models.CharField(max_length=255, verbose_name="パスワードハッシュ")
    user_name = models.CharField(max_length=50, verbose_name="ユーザー名")
    default_ai_id = models.IntegerField(null=True, blank=True, verbose_name="デフォルトAI ID")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return self.user_name





















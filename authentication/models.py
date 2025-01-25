from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)  # デフォルトで is_staff=False
        extra_fields.setdefault('is_superuser', False)  # デフォルトで is_superuser=False
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # スーパーユーザーは is_staff=True
        extra_fields.setdefault('is_superuser', True)  # スーパーユーザーは is_superuser=True

        if extra_fields.get('is_staff') is not True:
            raise ValueError("スーパーユーザーは is_staff=True である必要があります")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("スーパーユーザーは is_superuser=True である必要があります")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # ユーザーID（自動採番）
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    password_hash = models.CharField(max_length=255, verbose_name="パスワード")
    user_name = models.CharField(max_length=50, verbose_name="ユーザー名")
    is_staff = models.BooleanField(default=False, verbose_name="スタッフ権限")  # 必須
    is_active = models.BooleanField(default=True, verbose_name="アクティブ状態")  # 必須
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # ログインに使用するフィールド
    REQUIRED_FIELDS = ['user_name']  # スーパーユーザー作成時に必須フィールド

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー一覧"



















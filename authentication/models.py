from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, google_authenticated=False, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です。")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)  # デフォルトで is_staff=False
        extra_fields.setdefault('is_superuser', False)  # デフォルトで is_superuser=False
        extra_fields.setdefault('google_authenticated', google_authenticated) #Google認証ユーザーを区別する
        
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password() #Googleログインの場合、PW設定不要

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # スーパーユーザーは is_staff=True
        extra_fields.setdefault('is_superuser', True)  # スーパーユーザーは is_superuser=True
        extra_fields.setdefault('google_authenticated', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('スーパーユーザーを作成するには `is_staff=True` に設定してください。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('スーパーユーザーを作成するには `is_superuser=True` に設定してください。')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # ユーザーID（自動採番）
    email = models.EmailField(unique=True, verbose_name='メールアドレス')
    user_name = models.CharField(max_length=50, verbose_name="ユーザー名", blank=True, null=True)
    google_authenticated = models.BooleanField(default=False, verbose_name='Google認証ユーザー')
    is_staff = models.BooleanField(default=False, verbose_name='スタッフ権限')  # 必須
    is_active = models.BooleanField(default=True, verbose_name='アクティブ状態')  # 必須
    created_at = models.DateTimeField(default=now, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    # DjangoのデフォルトUserモデルとの競合回避のため、related_name を追加
    groups = models.ManyToManyField(
        Group,
        verbose_name="グループ",
        blank=True,
        related_name="custom_user_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="ユーザー権限",
        blank=True,
        related_name="custom_user_permissions"
    )   

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # ログインに使用するフィールド
    REQUIRED_FIELDS = ['user_name']  # スーパーユーザー作成時に必須フィールド

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー一覧'

    def __str__(self):
        return self.email

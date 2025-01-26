from django.db import models

class Reward(models.Model):
    REWARD_TYPE_CHOICES = [
        ('badge', 'Badge'),
        ('title', 'Title'),
    ]
    reward_id = models.AutoField(primary_key=True)  # リワードID（自動採番）
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, verbose_name="ユーザーID")
    reward_name = models.CharField(max_length=255, verbose_name="リワード名")
    reward_type = models.CharField(max_length=10, choices=REWARD_TYPE_CHOICES, verbose_name="リワードの種類")
    achieved_at = models.DateTimeField(auto_now_add=True, verbose_name="獲得日時")

    def __str__(self):
        return f"{self.user.user_name} - {self.reward_name}"

    class Meta:
        verbose_name = "リワード"
        verbose_name_plural = "リワード"
        # ユーザーが同じリワードを複数回獲得できないようにするための制約
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'reward_name', 'reward_type'],
                name='unique_user_reward'
            )
        ]

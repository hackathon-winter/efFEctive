from django.db import models
from django.utils.timezone import now

# Create your models here.

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)  # リワードID（自動採番）
    description = models.CharField(max_length=255, verbose_name="リワードの説明")
    is_claimed = models.BooleanField(default=False, verbose_name="取得済みかどうか")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return self.description


class Ranking(models.Model):
    ranking_id = models.AutoField(primary_key=True)  # ランキングID（自動採番）
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="rankings", verbose_name="ユーザー")
    score = models.IntegerField(verbose_name="スコア")
    ranking_type = models.CharField(max_length=50, verbose_name="ランキングの種類")
    date = models.DateTimeField(verbose_name="ランキングの日付")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    def __str__(self):
        return f"Ranking {self.ranking_id} - User {self.user.user_name}"


class UserRewardRelation(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="user_rewards", verbose_name="ユーザー")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name="user_rewards", verbose_name="リワード")
    is_claimed = models.BooleanField(default=False, verbose_name="取得済みかどうか")
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")
    updated_at = models.DateTimeField(default=now, verbose_name="更新日時")

    class Meta:
        unique_together = ('user', 'reward')  # ユーザーとリワードの組み合わせは一意

    def __str__(self):
        return f"User {self.user.user_name} - Reward {self.reward.description}"
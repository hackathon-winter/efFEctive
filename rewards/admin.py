from django.contrib import admin
from .models import Reward,Ranking,UserRewardRelation

# Register your models here.

admin.site.register(Reward)
admin.site.register(Ranking)
admin.site.register(UserRewardRelation)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils.timezone import now
from authentication.models import User
from questions.models import Answer, Question
from progress.models import Session
from .models import Badge

@login_required
def check_and_award_badges(request, user, category=None):
    
    # userの型が `User` であることを確認
    if not isinstance(user, User):
        raise TypeError('user は User モデルのインスタンスである必要があります。')
    
    level = None
    points_awarded = 0

    new_correct_count = Answer.objects.filter(session__user=user, is_correct=True, awarded=False).count()

    points_awarded += new_correct_count

    user.point += points_awarded
    user.save()

    Answer.objects.filter(session__user=user, is_correct=True, awarded=False).update(awarded=True)

    if category:
        category_correct_counts = (
            Answer.objects.filter(session__user=user, is_correct=True, question__category=category)
            .values('question__category')
            .annotate(correct_count=Count('answer_id'))
        )
    else:
        category_correct_counts = (
            Answer.objects.filter(session__user=user, is_correct=True)
            .values('question__category')
            .annotate(correct_count=Count('answer_id'))
        )

    for entry in category_correct_counts:
        category = entry['question__category']
        correct_count = entry['correct_count']

        if correct_count >= 15:
            level = Badge.GOLD
        elif correct_count >= 10:
            level = Badge.SILVER
        elif correct_count >= 5:
            level = Badge.BRONZE

    if level is None:
        return
    
    # 既にバッジを獲得済みかどうか確認
    existing_badge = Badge.objects.filter(users=user, category=category).first()

    if not existing_badge:
        Badge.objects.create(category=category, level=level).users.add(user)
    else:
        # 既存のバッジのランクをアップグレードする
        badge_levels = [Badge.BRONZE, Badge.SILVER, Badge.GOLD]

        if Badge.BADGE_LEVELS.index((existing_badge.level, existing_badge.get_level_display())) < Badge.BADGE_LEVELS.index((level, dict(Badge.BADGE_LEVELS[level]))):
            existing_badge.level = level
            existing_badge.acquired_at = now()
            existing_badge.save()

@login_required
def ranking_view(request):

    users = User.objects.all().order_by('-point')

    ranking = [
        (user.user_name, user.points, user) for user in users
    ]

    # 各ユーザーのバッジ情報を取得する
    user_badges = {user.user_name: list(user.badges_awarded.all()) for user in users}

    context = {
        'ranking': ranking,
        'user_badges': user_badges,
    }

    return render(request, 'rewards/ranking.html', context)
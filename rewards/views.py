from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils.timezone import now
from authentication.models import User
from questions.models import Answer, Question
from progress.models import Session
from .models import Badge

@login_required
def check_and_award_badges(user):

    category_correct_counts = (
        Answer.objects.filter(session__user=user, is_correct=True)
        .values('question__category')
        .annotate(correct_count=Count('id'))
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
        else:
            continue
    
    # 既にバッジを獲得済みかどうか確認
    existing_badge = Badge.objects.filter(user=user, category=category).first()

    if not existing_badge:
        Badge.objects.create(user=user, category=category, level=level)
    else:
        # 既存のバッジのランクをアップグレードする
        if Badge.BADGE_LEVELS.index((existing_badge.level, existing_badge.get_level_display())) < Badge.BADGE_LEVELS.index((level, dict(Badge.BADGE_LEVELS[level]))):
            existing_badge.level = level
            existing_badge.acquired_at = now()
            existing_badge.save()

@login_required
def ranking_view(request):

    users = User.objects.all()
    ranking = sorted(
        [(user.user_name, sum(session.score for session in user.sessions.all()), user) for user in users],
        key=lambda x: x[1], reverse=True
    )

    # 各ユーザーのバッジ情報を取得する
    user_badges = {user.user_name: list(user.badge_set.all()) for user in users}

    context = {
        'ranking': ranking,
        'user_badges': user_badges,
    }

    return render(request, 'rewards/ranking.html', context)
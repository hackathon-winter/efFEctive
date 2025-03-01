from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch
from django.utils.timezone import now
from authentication.models import User
from questions.models import Answer, Question
from .models import Badge, BadgesAwarded

@login_required
def check_and_award_badges(request, user, category=None):
    
    # userの型が `User` であることを確認
    if not isinstance(user, User):
        raise TypeError('user は User モデルのインスタンスである必要があります。')
    
    level = None
    points_awarded = 0

    new_correct_count = Answer.objects.filter(session__user=user, is_correct=True, awarded=False).count()

    points_awarded += new_correct_count

    user.points += points_awarded
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

        if correct_count >= 10:
            level = Badge.GOLD
        elif correct_count >= 5:
            level = Badge.SILVER
        elif correct_count >= 3:
            level = Badge.BRONZE

    if level is None:
        return
    
    # Badgeの取得
    badge, _ = Badge.objects.get_or_create(category=category, level=level)  

    # 既にバッジを獲得済みかどうか確認（BadgesAwardedに登録されているかどうか）
    existing_badge_award = BadgesAwarded.objects.filter(user=user, badge__category=category).first()

    if not existing_badge_award:
        BadgesAwarded.objects.create(user=user, badge=badge)
    else:
        # 既存のバッジがある場合は、アップグレードする
        badge_levels = [Badge.BRONZE, Badge.SILVER, Badge.GOLD]
        current_level_index = badge_levels.index(existing_badge_award.badge.level)
        new_level_index = badge_levels.index(level)

        if new_level_index > current_level_index:
            new_badge, _ = Badge.objects.get_or_create(category=category, level=level)
            existing_badge_award.badge = new_badge
            existing_badge_award.acquired_at = now()
            existing_badge_award.save()

@login_required
def ranking_view(request):

    # ユーザーと関連するバッジ情報を取得
    ranking = User.objects.prefetch_related(
        Prefetch(
            'badge_awards',  # Userモデルの related_name='badge_awards'
            queryset=BadgesAwarded.objects.select_related('badge'),
            to_attr='badge_awards_list'
        )
    ).order_by('-points')

    # 各ユーザーのバッジ情報を辞書にまとめる
    user_badges = {}
    for user in ranking:
        user_badges[user.id] = []
        # prefetch_relatedで取得した badge_awards_list からバッジ情報を取り出す
        for badge_award in getattr(user, 'badge_awards_list', []):
            user_badges[user.id].append(badge_award.badge)

    correct_answers = Answer.objects.filter(is_correct=True).count()
    total_answers = Answer.objects.count()
    accuracy_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    context = {
        'ranking': ranking,
        'user_badges': user_badges,
        'accuracy_rate': accuracy_rate,
        'correct_answers': correct_answers,
        'total_answers': total_answers,
    }

    return render(request, 'rewards/ranking.html', context)
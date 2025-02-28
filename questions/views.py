import random
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from progress.models import Session
from rewards.views import check_and_award_badges
from .models import Answer,Question
from .data import QUESTIONS_DATA

NORMAL = 'normal'
HARD = 'hard'

@login_required
def list_questions(request, difficulty=NORMAL):
    user = request.user

    # 最新のセッションを取得（なければ作成）
    latest_session = Session.objects.filter(user=user).order_by('-created_at').first()
    if not latest_session:
        latest_session = Session.objects.create(
            user=user,
            correct_answers=0,
            total_questions=0,
            session_answers=[],
            session_times=[],
            consecutive_correct=0,
            difficulty=difficulty,
            previous_difficulty=difficulty,
            start_time=now()
        )

    # 未回答の問題をDBから取得
    answer_ids = latest_session.session_answers
    unanswered_questions = Question.objects.filter(
        difficulty=latest_session.difficulty
    ).exclude(id__in=answer_ids)

    # 未解答の問題がなければ結果画面へ遷移
    if not unanswered_questions:
        return redirect('result_page')

    question = random.choice(list(unanswered_questions))

    # セッションに現在のquestion_idを保存
    request.session['current_question_id'] = str(question_id)

    return render(request, 'questions/question.html', {
        'question_number': latest_session.total_questions + 1,
        'question_id': question.id,
        'question_content': question.content,
        'question_choices': question.choices,
        'difficulty': latest_session.difficulty,
    })

@login_required
def continue_questions(request):
    return list_questions(request)

@login_required
def answer_save(request, question_id):
    if request.method == "POST":
        user = request.user
        start_time = now()

        # 最新のセッションを取得
        latest_session = Session.objects.filter(user=user).order_by('-created_at').first()
        if not latest_session:
            return redirect('list_questions')

        # DBにquestion_idがあるかチェック
        question_id = request.session.get('current_question_id')
        if not question_id:
            return redirect('list_questions')

        question = get_object_or_404(Question, id=question_id)

        selected_answer = request.POST.get('answer', '')

        # 正誤判定
        is_correct = (selected_answer == question.correct_answer)

        # セッションの正答数や連続正解数を更新
        latest_session.total_questions += 1
        if is_correct:
            latest_session.correct_answers += 1
            latest_session.consecutive_correct += 1
        else:
            latest_session.consecutive_correct = 0

        # 難易度の自動調整（連続正解3回でHARD、間違えたらNORMALにリセットする）
        if latest_session.consecutive_correct >= 3:
            latest_session.difficulty = HARD
        elif latest_session.consecutive_correct == 0:
            latest_session.difficulty = NORMAL

        # 解答済みの問題リストに追加
        if str(question_id) not in latest_session.session_answers:
            latest_session.session_answers.append(str(question_id))

        latest_session.save()

        time_taken = (now() - start_time).total_seconds()

        Answer.objects.create(
            session=latest_session,
            question=question,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken=time_taken
        )

        check_and_award_badges(request, user=request.user, category=question.category)

        return redirect('answer_result', question_id=question.id)

    return redirect('list_questions')

@login_required
def answer_result(request, question_id):

    user = request.user
    question = get_object_or_404(Question, id=question_id)

    latest_answer = Answer.objects.filter(
        session__user=user,
        question=question
    ).order_by('-created_at').first()

    if not latest_answer:
        return redirect('list_questions')

    context = {
        'selected_answer': latest_answer.selected_answer,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'is_correct': latest_answer.is_correct
    }
    return render(request, 'questions/answer.html', context)

@login_required
def end_session(request):

    user = request.user
    latest_session = Session.objects.filter(user=user).order_by('-created_at').first()

    if latest_session:
        latest_session.end_time = now()
        latest_session.save()

    return redirect('result_page')

@login_required
def result_page(request):

    user = request.user
    latest_session = Session.objects.filter(user=user).order_by('-created_at').first()

    if not latest_session:
        return redirect('list_questions')

    # セッション情報から正答率を計算する
    total_questions = latest_session.total_questions
    correct_answers = latest_session.correct_answers
    session_end_time = latest_session.end_time

    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    answers = Answer.objects.filter(session=latest_session).order_by('answer_id')

    context = {
        'accuracy': accuracy,
        'correct_answer': correct_answers,
        'total_questions': total_questions,
        'results': answers,
        'session_end_time': session_end_time
    }
    return render(request, 'questions/results.html', context)
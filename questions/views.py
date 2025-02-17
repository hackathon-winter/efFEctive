import random
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from progress.models import Session
from .models import Answer,Question
from .data import QUESTIONS_DATA

NORMAL = "normal"
HARD = "hard"

@login_required
def list_questions(request):

    #ユーザー情報、現在の日時を取得
    user = request.user
    now_time = now()

    #最新のセッション(正答数、総問題数、難易度)を取得
    latest_session = Session.objects.filter(user=user, session_end=False).order_by('-created_at').first()

    #進行中のセッションがない場合、セッションを新規作成
    if not latest_session:
        previous_session = Session.objects.filter(user=user).order_by('-created_at').first()
        previous_difficulty = previous_session.current_difficulty if previous_session else 'normal'

        latest_session = Session.objects.create(
            user=user,
            correct_answers=0,
            total_questions=0,
            consecutive_correct=0,
            current_difficulty=previous_difficulty,
            previous_difficulty=previous_difficulty,
            session_end=False,
            start_time=now(),
            created_at=now()
        ) 

    #難易度に応じた問題をランダムに取得
    filtered_questions = [q for q in QUESTIONS_DATA if q['difficulty'] == latest_session.current_difficulty]
    question_data = random.choice(filtered_questions) if filtered_questions else None

    if not question_data:
        return render(request, 'error.html', {'message': '問題が見つかりません。'})

    return render(request,'question.html', {
        'question_number':latest_session.total_questions + 1,
        'question_id':question_data['id'],
        'question_content':question_data['content'],
        'question_choices':question_data['choices'],
        'difficulty':latest_session.current_difficulty,
        }) 

@login_required
def answer_save(request,question_id):

    if request.method == "POST":
        start_time = now()
        user = request.user
        latest_session = Session.objects.filter(user=user).order_by('-created_at').first()

        if not latest_session:
            return render('list_questions')
        
        #問題を取得
        question = get_object_or_404(Question, id=question_id)
        correct_answer = question.correct_answer

        #ユーザーが解答した内容を取得
        selected_answer = request.POST.get('answer', '')  

        #正誤判定
        is_correct = selected_answer == correct_answer

        #ユーザーの最新の進捗を取得(セッションの正答数、総問題数を更新)
        latest_session.total_questions += 1
        if is_correct:
            latest_session.correct_answers += 1
            latest_session.consecutive_correct += 1
        else:
            latest_session.consecutive_correct = 0

        #難易度自動調整
        if latest_session.consecutive_correct >= 3:
            latest_session.current_difficulty = HARD
        elif latest_session.consecutive_correct == 0:
            latest_session.current_difficulty = NORMAL
        
        latest_session.save()

        #ユーザーの解答時間を取得
        time_taken = (now() - start_time).total_seconds()

        #ユーザーの解答を保存
        Answer.objects.create(
            session=latest_session,
            question=question,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken=time_taken
        )
        return redirect('list_questions') 
       
    return redirect('list_questions') 

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'questions/question_detail.html', {'question':question})
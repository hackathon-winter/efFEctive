from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
#モデルをインポート
from django.contrib.auth.decorators import login_required
from progress.models import Session
from .models import Answer,Question

# Create your views here.

@login_required
def list_questions(request):
    #最新のセッションが終了しているかを取得
    user = request.user.id  #ユーザーid取得   
    #最新のセッションが終了しているかを取得
    user_session_end = Session.objects.filter(user=user).values_list('session_end',flat=True).order_by('-created_at').first()
    #最新のセッションが終了している場合、セッションを作成
    if user_session_end == True:
        now = datetime.now()
        user_info = request.user
        make_session = Session(user=user_info,correct_answers=0,total_questions=0,start_time=now,created_at=now)
        make_session.save()  
    #ユーザーの最新の進捗を取得
    user_session = Session.objects.filter(user=user).values_list('session_id',flat=True).order_by('-created_at').first()
    #問題解答数を取得
    user_answers_count = Answer.objects.filter(session=user_session).count()
    #直近の問題の正答を取得
    user_answers = Answer.objects.filter(session=user_session).values('is_correct').order_by('-created_at')[:3]
    sum_answer =  user_answers.count()
    user_answers = sum(item['is_correct'] for item in user_answers)

    #難易度の設定
    if user_answers >= 3:
        question_difficult = 'hard'
    else:
        question_difficult = 'normal'
    #難易度から問題をランダムに取得
    question = Question.objects.filter(difficulty=question_difficult).order_by('?').first()
    #問題のID、内容、選択肢を格納
    question_id = question.id
    question_content = question.content
    question_choices = list(question.choices.items())

    return render(request,'問題表示用HTML', {'user_answers_count':user_answers_count,'question_id':question.id,'question_content':question_content,'question_choices':question_choices}) 

@login_required
def answer_save(request,question_id):

    if request.method == "POST":
        #ユーザーが解答した内容を取得
        answer = request.POST.get('answer', '')  
        #question_idを取得
        question_id = request.POST.get('question_id', '')  
        #ユーザーid取得
        user = request.user.id
        #ユーザーの最新の進捗を取得
        user_session = Session.objects.filter(user=user).values_list('session_id',flat=True).order_by('-created_at').first()
        session = Session.objects.get(session_id=user_session)
        #questionインスタンスを取得
        question = Question.objects.get(id=question_id)
        #問題の答えを取得
        question_correct = Question.objects.filter(id=question_id).values_list('correct_answer',flat=True)
        #ユーザーの解答が正解だった場合、セッションの正答数を更新
        if answer == question_correct[0]:
            is_correct = True
            session.correct_answers = session.correct_answers + 1 
            session.save()
        else:
            is_correct = False
        #セッションの総問題数を更新
        session.total_questions = session.total_questions + 1
        session.save()
        #ユーザーの解答を保存
        answer = Answer(session=session,question=question,selected_answer=answer,is_correct=is_correct,time_taken=1)
        answer.save()
       
    return redirect('list_questions') 


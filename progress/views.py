from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#モデルをインポート
from .models import Session
from questions.models import Answer

@login_required
def view_progress(request):
    
    session_answers = [] #ユーザーが解答した正誤を格納する配列を用意
    session_times = [] #各セッションの時間を格納する配列を用意
    user = request.user.id
    #ユーザーのsession_id全てを取得
    user_sessions = Session.objects.filter(user=user).values_list('session_id',flat=True)
    #セッションごとの情報を取得
    for session in user_sessions:
        #正答情報を取得
        answer_list = Answer.objects.filter(session=session).values_list('is_correct',flat=True)
        session_answers.append(list(answer_list))
        #セッションの日時を取得
        time = Session.objects.filter(session_id=session).values_list('start_time',flat=True)
        session_times.append(time.first().strftime("%Y/%m/%d %H:%M:%S"))
    
    #全体の正答数、間違え数、正答率を取得
    count_of_true = sum(sublist.count(True) for sublist in list(session_answers))
    count_of_false = sum(sublist.count(False) for sublist in list(session_answers))
    sum_answer = count_of_true + count_of_false
    true_rate = count_of_true / sum_answer * 100

    return render(request,'進捗確認のHTML', {'session_answers': session_answers,'session_times':session_times,'true_rate':true_rate,'sum_answer':sum_answer,'count_of_true':count_of_true}) 

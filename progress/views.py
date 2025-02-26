from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Session
from authentication.models import User
from questions.models import Answer

@login_required
def view_progress(request):

    user = request.user    
    session_data = [] #各セッションごとのデータをリストに格納

    #ユーザーのセッション情報を全てを取得
    user_sessions = Session.objects.filter(user=user)

    #セッションごとの情報を取得
    for session in user_sessions:
        #正答情報を取得
        answer_list = list(Answer.objects.filter(session=session).values_list('is_correct',flat=True))
        correct_answers = sum(answer_list)
        total_count = len(answer_list)
        accuracy = (correct_answers / total_count * 100) if total_count > 0 else 0

        #セッションの日時を取得
        session_data.append({
            'end_time': session.end_time.strftime('%Y/%m/%d %H:%M:%S') if session.end_time else '未完了',
            'answers': answer_list,
            'accuracy': accuracy,
        })
    
    #全体の正答数、間違えた数、正答率を取得
    count_of_true = sum(sublist['answers'].count(True) for sublist in session_data)
    count_of_false = sum(sublist['answers'].count(False) for sublist in session_data)
    sum_answer = count_of_true + count_of_false
    true_rate = (count_of_true / sum_answer * 100) if sum_answer > 0 else 0

    return render(request,'progress/record.html', {
        'session_data': session_data,
        'true_rate':true_rate,
        'sum_answer':sum_answer,
        'count_of_true':count_of_true
    })
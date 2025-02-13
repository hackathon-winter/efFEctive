from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# ユーザーがログインをしていない場合はログインページにリダイレクトする
@login_required
def home_view(request):
    return render(request, 'home.html', {'user':request.user})
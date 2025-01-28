from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    # GETリクエストの場合は、ログインフォームを表示
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    
    # POSTリクエストの場合は、ログイン処理を実行
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 認証を試みる
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # ログイン成功
            login(request, user)
            return redirect('home')  # ログイン後のリダイレクト先
        else:
            # ログイン失敗
            messages.error(request, 'ユーザー名またはパスワードが正しくありません。')
            return render(request, 'authentication/login.html')
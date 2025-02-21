from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'メールアドレスとパスワードを入力してください。')
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user:
            
            storage = messages.get_messages(request)            
            storage.used = True

            login(request, user)
            messages.success(request, 'ログインが成功しました。')
            return redirect('home')
        else:
            messages.error(request, 'メールアドレスまたはパスワードが間違っています。')
            return redirect('login')

    return render (request, 'authentication/login.html')

@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('login')

    return redirect('home')
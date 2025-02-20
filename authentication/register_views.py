from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

def register_view(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        user_name = request.POST.get('username')

        if not email or not password or not user_name:
            messages.error(request, 'メールアドレス、パスワード、ユーザー名をすべて入力してください。')

        # 既存ユーザーかどうかを確認する
        if User.objects.filter(email=email).exists():
            messages.error(request, 'このメールアドレスは既に登録されています。')
            return redirect('register')

        # 新規ユーザーを作成する
        user = User(email=email, user_name=user_name)
        user.set_password(password)
        user.save()

        messages.success(request, '新規登録が完了しました。ログインしてください。')
        return redirect('login')
        

    return render(request, 'authentication/register.html')
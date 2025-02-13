from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def register_view(request):
    if request.method == 'POST':

        email = data.get('email')
        password = data.get('password')
        user_name = data.get('username')

        if not email or not password or not user_name:
            messages.error(request, 'メールアドレス、パスワード、ユーザー名をすべて入力してください。')

        # 既存ユーザーかどうかを確認する
        if User.objects.filter(email=email).exists():
            message.error(request, 'このメールアドレスは既に登録されています。')
            return redirect('register')

        # 新規ユーザーを作成する
        user = User.objects.create_user(email=email, password=password, user_name=user_name)
        messages.success(request, '新規登録が完了しました。ログインしてください。')
        return redirect('login')
        

    return render(request, 'authentication/register.html')
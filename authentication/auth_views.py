import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'無効なリクエストです。'})

        email = data.get('email')
        password = data.get('password')
        
        if not email or password:
            return JsonResponse({'メールアドレスとパスワードを入力してください。'}, status=400)

        user = authenticate(request, username=email, password=password)
        if user:
           login(request, user)
           return JsonResponse({
            'message': 'ログインが成功しました。',
            'user_id': user.id,
            'user_name': user.user_name
        })
        else:
            return JsonResponse({'error': 'メールアドレスまたはパスワードが間違っています。'}, status=400)

    return JsonResponse({'error': 'このページに直接アクセスすることはできません。ログインフォームから操作してください。'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'ログアウトしました。'}, status=200)
    return JsonResponse({'error': 'このページに直接アクセスすることはできません。'}, status=405)
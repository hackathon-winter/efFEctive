import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.views.jwt_utils import generate_jwt
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # JSONデータを取得する
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, username=email, password=password)

            if user:
                token = generate_jwt_token(user)

                return JsonResponse({
                    'message': 'ログインが成功しました。',
                    'token': token,
                    'user_id': user.id,
                    'user_name': user.user_name
                })
            else:
                return JsonResponse({'error': 'メールアドレスまたはパスワードが間違っています。'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': '無効なリクエストです。'}, status=400)

    return JsonResponse({'error': 'このページに直接アクセスすることはできません。ログインフォームから操作してください。'}, status=405)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'ログアウトしました。'}, status=200)
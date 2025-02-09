import json
import requests
import os
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code')

            # Googleのトークンエンドポイントにリクエストを行う
            response = requests.post('https://oauth2.googleapis.com/token', data={
                'code': code,
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
            })

            token_data = response.json()

            if 'id_token' not in token_data:
                return JsonResponse({'error': 'GoogleからIDトークンが取得できませんでした。'}, status=400)

            id_token = token_data['id_token']

            # IDトークンを検証する
            user_info = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}").json()

            email = user_info.get('email')
            name = user_info.get('name')

            if not email:
                return JsonResponse({'error': 'Googleアカウントの情報が取得できませんでした。'}, status=400)

            # ユーザーが存在しない場合、新規作成をする
            user, created = User.objects.get_or_create(email=email, defaults={'user_name': name})

            login(request, user)

            return JsonResponse({'message': 'Googleログインが成功しました。', 'email': email}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '無効なリクエストです。'}, status=400)

    return JsonResponse({'error': 'このページに直接アクセスすることはできません。ログインフォームから操作してください。'}, status=405)
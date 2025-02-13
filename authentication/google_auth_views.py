import json
import requests
import os
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from authentication.models import User

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

@csrf_protect
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code')
            
            if not code:
                messages.error(request, '認証コードが提供されていません。')
                return redirect('login')

            # Googleのトークンエンドポイントにリクエストを行う
            response = requests.post('https://oauth2.googleapis.com/token', data={
                'code': code,
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
            })
            if response.status_code != 200:
                messages.error(request, 'Googleの認証サーバーとの接続に失敗しました。')
                return redirect('login')

            token_data = response.json()
            id_token = token_data.get('id_token')

            if not id_token:
                messages.error(request, 'GoogleからIDトークンが取得できませんでした。')
                return redirect('login')

            # IDトークンを検証する
            user_info = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
            if user_info.status_code !=200:
                messages.error(request, 'GoogleのIDトークンの検証に失敗しました。')
                return redirect('login')

            user_info = user_info.json()
            email = user_info.get('email')
            name = user_info.get('name')

            if not email:
                messages.error(request, 'Googleアカウントの情報が取得できませんでした。')
                return redirect('login')

            # ユーザーが存在しない場合、新規作成をする
            user, created = User.objects.get_or_create(email=email, defaults={'user_name': name, 'google_authenticated':True})

            login(request, user)

            messages.success(request, 'Googleログインが成功しました。')
            return redirect('home')
        
        except json.JSONDecodeError:
            messages.error(request, '無効なリクエストです。')
            return redirect('login')

    return redirect('login')
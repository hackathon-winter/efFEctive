import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'リクエストの形式が正しくありません。'})

            email = data.get('email')
            password = data.get('password')
            user_name = data.get('user_name')

            if not email or not password or not user_name:
                return JsonResponse({'error': 'メールアドレス、パスワード、ユーザー名をすべて入力してください。'}, status=400)

            # 既存ユーザーかどうかを確認する
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'このメールアドレスは既に登録されています。'}, status=400)

            # 新規ユーザーを作成する
            user = User.objects.create_user(email=email, password=password, user_name=user_name)
            return JsonResponse({'message': '新規登録が完了しました。ログインしてください。'}, status=201)

    return JsonResponse({'error': 'このページには直接アクセスできません。新規登録フォームから登録を行ってください。'}, status=405)
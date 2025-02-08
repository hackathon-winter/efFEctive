import jwt
import datetime
import environ
from django.conf import settings
from django.contrib.auth import get_user_model

# 環境変数の読み込み
env = environ.Env()
env.read_env()

User = get_user_model()

#
def generate_jwt(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

# JWTトークンをデコードし、ユーザー情報を取得する
def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return User.objects.get(id=payload["user_id"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except User.DoesNotExist:
        return None
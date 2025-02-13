from django.shortcuts import redirect
from django.conf import settings
import urllib.parse

def google_register(request):

    base_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
    }

    auth_url = f'{base_url}?{urllib.parse.urlencode(params)}'
    return redirect(auth_url)
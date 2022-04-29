from django.shortcuts import render, redirect
from django.conf import settings

def login(request):
    return render(request, 'login.html')

def kakao_login(request): 
    key  = settings.KAKAO_LOGIN_REST_KEY
    redirect_url = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'

    # redirect_uri = main_domain + "users/login/kakao/callback" 
    url = f'https://kauth.kakao.com/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code'
    return redirect(url)

import httpx
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from base.utils import destructuring
from base import redirects
from .models import User, Setting

key = settings.KAKAO_LOGIN_REST_KEY

if settings.DEBUG:
    redirect_url = "http://127.0.0.1:8000/account/login/kakao/callback/"
else:
    redirect_url = "https://finance.1ife.kr/account/login/kakao/callback/"


def kakao_login(request):
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code"
    return redirect(url)


@login_required
def kakao_logout(request):
    logout(request)
    return redirects.login()


def _get_kakao_token(request) -> dict | None:
    code = request.GET.get("code", None)

    if not code:
        return None

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": key,
        "redirect_url": redirect_url,
        "code": code,
    }
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    response = httpx.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def _get_user(access_token) -> dict | None:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = httpx.post(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    return None


def _get_or_user(**kwargs) -> User:
    email = kwargs.get("email")
    try:
        user = User.objects.get(email=email)
        user.update(**kwargs)
    except User.DoesNotExist:
        user = User.objects.create(**kwargs)

    return user


def kakao_login_callback(request):
    if request.user.is_authenticated:
        return redirects.main()

    kakao_token = _get_kakao_token(request)
    if not kakao_token:
        return redirects.login()

    access_token = kakao_token.get("access_token")

    kakao_user = _get_user(access_token)
    if not kakao_user:
        return redirects.login()

    kakao_user = kakao_user.get("kakao_account")
    nickname = kakao_user.get("profile").get("nickname")
    avatar_url = kakao_user.get("profile").get("profile_image_url")
    email = kakao_user.get("email")
    gender = kakao_user.get("gender")
    age_range = kakao_user.get("age_range")
    user = _get_or_user(
        nickname=nickname,
        email=email,
        gender=gender,
        age_range=age_range,
        avatar_url=avatar_url,
    )
    login(request, user)
    return redirects.main()

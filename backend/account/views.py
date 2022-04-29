import httpx
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login

from .models import User

key = settings.KAKAO_LOGIN_REST_KEY
redirect_url = "http://127.0.0.1:8000/account/login/kakao/callback/"


def kakao_login(request):
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code"
    return redirect(url)


def _get_kakao_token(request) -> dict | None:
    code = request.GET.get("code", None)

    if not code:
        return None

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": key,
        "redirect_url": redirect_url,
        # "client_secret": SOCIAL_OUTH_CONFIG["KAKAO_SECRET_KEY"],
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
    user, is_create = User.objects.get_or_create(**kwargs)
    if is_create:
        user.set_unusable_password()
        user.save()
    return user


def kakao_login_callback(request):
    kakao_token = _get_kakao_token(request)
    if not kakao_token:
        return redirect("account:login")

    access_token = kakao_token.get("access_token")

    kakao_user = _get_user(access_token)
    if not kakao_user:
        return redirect("account:login")

    kakao_user = kakao_user.get("kakao_account")

    nickname = kakao_user.get("profile").get("nickname")
    email = kakao_user.get("email")
    gender = kakao_user.get("gender")
    age_range = kakao_user.get("age_range")

    user = _get_or_user(nickname=nickname, email=email, gender=gender, age_range=age_range)
    login(request, user)
    return redirect("exchange_rate:main")

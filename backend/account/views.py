from weakref import ref
import httpx
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from operator import is_, itemgetter

from base import redirects
from .models import User

key = settings.KAKAO_LOGIN_REST_KEY

if settings.DEBUG:
    redirect_url = "http://127.0.0.1:8000/account/login/kakao/callback/"
else:
    redirect_url = "https://finance.1ife.kr/account/login/kakao/callback/"


def kakao_login(request):
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code"
    # if "KAKAOTALK" in request.META["HTTP_USER_AGENT"]:
    #     url = f"/oauth/authorize?client_id=${key}&redirect_uri=${redirect_url}&response_type=code&prompt=none"
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


def _update_user(user: User, **kwargs):
    keys = list(kwargs.keys())

    is_update = False

    for i in keys:
        if (attr := getattr(user, i)) != (attr2 := kwargs.get(i)):
            if not (attr and attr2):
                return
            is_update = True
            print(attr, attr2)
            setattr(user, i, attr2)

    if is_update:
        user.save()


def _get_or_create_user(**kwargs) -> tuple(User, bool):
    email = kwargs.get("email")
    is_create = False
    try:
        user = User.objects.get(email=email)
        _update_user(user, **kwargs)

    except User.DoesNotExist:
        user = User.objects.create(**kwargs)
        is_create = True

    # except IntegrityError:
    #     return None

    return (user, is_create)


def kakao_login_callback(request):
    if request.user.is_authenticated:
        return redirects.main()
    kakao_token = _get_kakao_token(request)

    if not kakao_token:
        return redirects.login()

    access_token = kakao_token.get("access_token")
    refresh_token = kakao_token.get("refresh_token")
    kakao_user = _get_user(access_token)

    if not kakao_user:
        return redirects.login()

    kakao_user = kakao_user.get("kakao_account")
    nickname = kakao_user.get("profile").get("nickname")
    avatar_url = kakao_user.get("profile").get("profile_image_url")
    email = kakao_user.get("email")
    gender = kakao_user.get("gender")
    age_range = kakao_user.get("age_range")

    if not gender or not age_range:
        url = f"https://kauth.kakao.com/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code&scope=gender,age_range,talk_message"
        return redirect(url)

    user, is_create = _get_or_create_user(
        nickname=nickname,
        email=email,
        gender=gender,
        age_range=age_range,
        avatar_url=avatar_url,
        refresh_token=refresh_token,
    )
    print(is_create)
    login(request, user)

    return redirects.main()

from django.conf import settings
from httpx import post

from .exceptions import KakaoCallbackException, KakaoTokenException, KakaoUserException


KEY: str = settings.KAKAO_LOGIN_REST_KEY
REDIRECT_URL: str = settings.KAKAO_LOGIN_REDIRECT_URL


def kakao_account_token(refresh_token: str) -> str | None:
    url: str = "https://kauth.kakao.com/oauth/token"

    data: dict = {
        "client_id": KEY,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    headers: dict = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    res = post(url, data=data, headers=headers)

    if res.status_code != 200:
        raise KakaoTokenException

    res = res.json()
    return res.get("access_token")


def get_kakao_token(request) -> dict:
    code = request.GET.get("code", None)

    if not code:
        raise KakaoCallbackException

    url: str = "https://kauth.kakao.com/oauth/token"
    data: dict = {
        "grant_type": "authorization_code",
        "client_id": KEY,
        "redirect_url": REDIRECT_URL,
        "code": code,
    }
    headers: dict = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    response = post(url, data=data, headers=headers)
    if response.status_code != 200:
        raise KakaoTokenException
    return response.json()


def get_kakao_user(access_token) -> dict:
    headers: dict = {"Authorization": f"Bearer {access_token}"}
    response = post(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers,
    )
    if response.status_code != 200:
        raise KakaoUserException
    return response.json()

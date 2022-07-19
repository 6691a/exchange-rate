from .models import User
from django.conf import settings
from httpx import post


class NoTokenException(Exception):
    ...


def kakao_account_token(user: User) -> str | None:
    user.refresh_token
    url = "https://kauth.kakao.com/oauth/token"
    key = settings.KAKAO_LOGIN_REST_KEY

    data = {
        "client_id": key,
        "grant_type": "refresh_token",
        "refresh_token": user.refresh_token,
    }

    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    res = post(url, data=data, headers=headers)

    if res.status_code != 200:
        return None
        # raise NoTokenException

    res = res.json()

    return res.get("access_token")

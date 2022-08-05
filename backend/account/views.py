from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from alert.tasks import send_kakao_welcome
from base import redirects
from .models import User
from .base import get_kakao_token, get_kakao_user
from .exceptions import KakaoTokenException, KakaoUserException

KEY = settings.KAKAO_LOGIN_REST_KEY
REDIRECT_URL = settings.KAKAO_LOGIN_REDIRECT_URL


def kakao_login(request):
    print(REDIRECT_URL)
    print(settings.DEBUG)
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={KEY}&redirect_uri={REDIRECT_URL}&response_type=code"
    # if "KAKAOTALK" in request.META["HTTP_USER_AGENT"]:
    #     url = f"/oauth/authorize?client_id=${key}&redirect_uri=${redirect_url}&response_type=code&prompt=none"
    return redirect(url)


@login_required
def kakao_logout(request):
    logout(request)
    return redirects.login()


def kakao_login_callback(request):
    if request.user.is_authenticated:
        return redirects.main()

    try:
        kakao_token = get_kakao_token(request)
    except KakaoTokenException:
        return redirects.login()

    if not kakao_token:
        return redirects.login()

    access_token = kakao_token.get("access_token")
    refresh_token = kakao_token.get("refresh_token")

    try:
        kakao_user = get_kakao_user(access_token)
    except KakaoUserException:
        return redirects.login()

    if not kakao_user:
        return redirects.login()

    kakao_user = kakao_user.get("kakao_account")
    nickname = kakao_user.get("profile").get("nickname")
    avatar_url = kakao_user.get("profile").get("profile_image_url")
    email = kakao_user.get("email")
    gender = kakao_user.get("gender")
    age_range = kakao_user.get("age_range")

    if not gender or not age_range:
        url = f"https://kauth.kakao.com/oauth/authorize?client_id={KEY}&redirect_uri={REDIRECT_URL}&response_type=code&scope=gender,age_range,talk_message"
        return redirect(url)

    user, is_create = User.objects.get_and_update_or_create(
        nickname=nickname,
        email=email,
        gender=gender,
        age_range=age_range,
        avatar_url=avatar_url,
        refresh_token=refresh_token
    )

    if is_create:
        send_kakao_welcome.delay(user.refresh_token)

    login(request, user)

    return redirects.main()

from ninja import Router

router = Router()

from django.http import HttpRequest

from alert.talk import KakaoTalk
from account.base import kakao_account_token
from account.models import User


@router.get("test")
def test(request: HttpRequest):
    token = kakao_account_token(User.objects.get(id=1))
    print(token)
    KakaoTalk.welcome(token)
    # KakaoTalk.send(token, KakaoTalk.text("미국 달러", 1310), "USD")

    return 200

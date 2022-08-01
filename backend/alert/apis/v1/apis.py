from ninja import Router

router = Router()

from django.http import HttpRequest

# from alert.talk import KakaoTalk
# from account.base import kakao_account_token
from account.models import User
from alert.tasks import kakao_welcome


@router.get("test")
def test(request: HttpRequest):
    user = User.objects.get(id=3)
    kakao_welcome.delay(user.refresh_token)
    return 200

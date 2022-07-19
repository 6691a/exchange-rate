from ninja import Router

router = Router()

from alert.talk import KakaoTalk
from account.base import kakao_account_token
from account.models import User


@router.get("test")
def test(request):
    token = kakao_account_token(User.objects.get(id=1))
    print(token)
    KakaoTalk.welcome(token)
    return 200

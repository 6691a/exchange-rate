from celery import shared_task

from account.base import kakao_account_token
from .models import Alert
from .talk import KakaoTalk


@shared_task
def send_kakao_talk(refresh_token: str, name: str, price: int, url_path: str) -> bool:
    if token := kakao_account_token(refresh_token):
        KakaoTalk.send(token, name, price, url_path)
        return True
    return False


@shared_task
def send_kakao_welcome(refresh_token: str):
    if token := kakao_account_token(refresh_token):
        KakaoTalk.welcome(token)



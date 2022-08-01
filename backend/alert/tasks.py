from celery import shared_task

from .talk import KakaoTalk
from account.base import kakao_account_token
from account.models import User


@shared_task
def kakao_send(refresh_token: str, currency: str, price: int, url_path: str):
    if token := kakao_account_token(refresh_token):
        KakaoTalk.send(token, currency, price, url_path)


@shared_task
def kakao_welcome(refresh_token: str):
    print(refresh_token)
    if token := kakao_account_token(refresh_token):
        print(token)
        KakaoTalk.welcome(token)

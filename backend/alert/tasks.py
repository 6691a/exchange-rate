from celery import shared_task

from .talk import KakaoTalk
from account.base import kakao_account_token


@shared_task
def send_kakao_talk(refresh_token: str, currency: str, price: int, url_path: str):
    if token := kakao_account_token(refresh_token):
        KakaoTalk.send(token, currency, price, url_path)


@shared_task
def send_kakao_welcome(refresh_token: str):
    if token := kakao_account_token(refresh_token):
        KakaoTalk.welcome(token)



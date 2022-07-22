from celery import shared_task

from .talk import KakaoTalk
from account.base import kakao_account_token
from account.models import User


@shared_task
def kakao_send(user: User, currency: str, price: int, url_path: str):
    if token := kakao_account_token(user):
        KakaoTalk.send(token, currency, price, url_path)


@shared_task
def kakao_welcome(user: User):
    if token := kakao_account_token(user):
        KakaoTalk.welcome(token)

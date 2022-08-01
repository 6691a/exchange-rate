from email import contentmanager
from celery import shared_task

from .models import WatchList, User
from httpx import post
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings


@shared_task
def insert_watch_list(**kwargs) -> int:
    watch, _ = WatchList.objects.get_or_create(**kwargs)
    return watch.id


@shared_task
def kakao_refresh_token():
    url = "https://kauth.kakao.com/oauth/token"
    key = settings.KAKAO_LOGIN_REST_KEY
    now = datetime.now()
    start = now - relativedelta(months=1)
    end = now + relativedelta(days=1)

    users = User.objects.filter(last_login__range=[start, end])

    for user in users:
        if not user.refresh_token:
            continue

        data = {
            "client_id": key,
            "grant_type": "refresh_token",
            "refresh_token": user.refresh_token,
        }

        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        res = post(url, data=data, headers=headers)

        if res.status_code != 200:
            continue

        res = res.json()

        if refresh_token := res.get("refresh_token"):
            user.refresh_token = refresh_token
            user.save()

        return res.access_token

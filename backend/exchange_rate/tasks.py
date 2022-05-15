import re
import json
import httpx
from celery import shared_task
from datetime import datetime
from typing import Union
from django.conf import settings
from django.core.cache import cache

from .models import ExchangeRate, ExchangeRateSchedule


class Currency:
    def get(self) -> Union[dict, None]:
        """
        httpx 200 ok
            - return dict
        httpx not 200
            - return None
        """
        r = httpx.get("http://fx.kebhana.com/FER1101M.web")

        if r.status_code != 200:
            return

        req = r.text.replace("var exView = ", "")
        req = re.sub(r",(\s)+]", "]", req)
        return json.loads(req)

    def __str_to_datetime(self, str: str, format: str) -> datetime:
        return datetime.strptime(str, format)

    def update(self) -> None:
        res = self.get()
        if not res:
            return False

        fix_time = self.__str_to_datetime(res.get("날짜"), "%Y년 %m월 %d일 %H:%M")
        for i in res.get("리스트"):
            currency = i.get("통화명")
            standard_price = i.get("매매기준율")
            ExchangeRate.objects.create(fix_time=fix_time, currency=currency, standard_price=standard_price)
        return True


@shared_task
def day_off():
    today = datetime.today().date()
    if ExchangeRateSchedule.objects.filter(day_off=datetime.today()).exists():
        cache.set("day_off", today)
        return today
    cache.set("day_off", -1)
    return -1


def is_day_off():
    day_off = cache.get("day_off")
    today = datetime.today().date()

    if not day_off:
        if ExchangeRateSchedule.objects.filter(day_off=today).exists():
            cache.set("day_off", today)
            return True
        cache.set("day_off", -1)
        return False

    if day_off == today:
        return True
    return False


@shared_task
def exchange_rate():
    if not is_day_off():
        c = Currency()
        if not c.update():
            return -2
        return datetime.today().date()
    return -1

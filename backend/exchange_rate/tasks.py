from re import sub as re_sub
from json import loads as json_loads
from httpx import get as httpx_get
from celery import shared_task
from datetime import datetime
from django.core.cache import cache
from asgiref.sync import async_to_sync

from channel.base import channel_group_send
from .models import ExchangeRate, ExchangeRateSchedule
from .channel.base import exchange_rate_msg

# 14시간
TIME_OUT = 50400


class Currency:
    def get(self) -> dict | None:
        """
        httpx 200 ok
            - return dict
        httpx not 200
            - return None
        """
        r = httpx_get("http://fx.kebhana.com/FER1101M.web")

        if r.status_code != 200:
            return

        req = r.text.replace("var exView = ", "")
        req = re_sub(r",(\s)+]", "]", req)
        return json_loads(req)

    def __str_to_datetime(self, str: str, format: str) -> datetime:
        return datetime.strptime(str, format)

    def update(self) -> list[ExchangeRate]:
        res = self.get()
        if not res:
            return False

        fix_time = self.__str_to_datetime(res.get("날짜"), "%Y년 %m월 %d일 %H:%M")
        data = []
        for i in res.get("리스트"):
            split = i.get("통화명").split(" ")
            country = split[0]
            currency = split[1]
            standard_price = i.get("매매기준율")
            data.append(
                ExchangeRate(
                    fix_time=fix_time,
                    country=country,
                    currency=currency,
                    standard_price=standard_price,
                )
            )

        return ExchangeRate.objects.bulk_create(data)


@shared_task
def day_off():
    today = datetime.today().date()
    if ExchangeRateSchedule.objects.filter(day_off=datetime.today()).exists():
        cache.set("day_off", today, TIME_OUT)
        return today
    cache.set("day_off", -1, TIME_OUT)
    return -1


def is_day_off():
    day_off = cache.get("day_off")
    today = datetime.today().date()

    if not day_off:
        if ExchangeRateSchedule.objects.filter(day_off=today).exists():
            cache.set("day_off", today, TIME_OUT)
            return True
        cache.set("day_off", -1, TIME_OUT)
        return False

    if day_off == today:
        return True
    return False


def send_exchange_rate(data: ExchangeRate):
    group_name = data.currency.upper()
    async_to_sync(channel_group_send)(
        group_name=group_name,
        data=async_to_sync(exchange_rate_msg)(data, data.currency),
    )


def send_watch_list(data: ExchangeRate):
    group_name = data.currency.upper()


def group_send(data: list[ExchangeRate]):
    for exchage in data:
        send_exchange_rate(exchage)
        send_watch_list(exchage)


@shared_task
def exchange_rate():
    if not is_day_off():
        c = Currency()
        if data := c.update():
            group_send(data)
            return datetime.today().date()
        return -2
    return -1

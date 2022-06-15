from channels.db import database_sync_to_async
from datetime import date, timedelta, datetime

from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate
FirstExchanteRate = ExchangeRate
LastExchanteRate = ExchangeRate


def date_offset(date, offset) -> date:
    return date - timedelta(days=offset)


def _work_date(date) -> date:
    offset = date.weekday() - 4
    if 0 < offset:
        return date_offset(date, offset)
    return date


@database_sync_to_async
def latest_exchange_aggregate(currency: str) -> tuple[MinExchanteRate, MaxExchanteRate]:
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=_work_date(date=date.today())
    )
    return (
        today_exchange.order_by("standard_price")[0],
        today_exchange.order_by("-standard_price")[0]
    )


@database_sync_to_async
def latest_exchange(*args, **kwargs) -> list[ExchangeRate]:
    kwargs["created_at__date"] = _work_date(date=date.today())
    return list(ExchangeRate.objects.filter(*args, **kwargs))

# fluctuation_rate()
# 어제 종가 / 현제가 * 100

@database_sync_to_async
def first_and_last_exchange(*args, **kwargs) -> tuple[FirstExchanteRate, LastExchanteRate]:
    kwargs["created_at__date"] = _work_date(date=date.today())
    e = list(ExchangeRate.objects.filter(*args, **kwargs))
    return (e[0], e[-1])


@database_sync_to_async
def fluctuation_rate(currency) -> tuple[FirstExchanteRate, LastExchanteRate]:
    today = _work_date(date=date.today())
    yester_day = _work_date(date=date.today()) - timedelta(1)

    e = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__in=[yester_day, today]
    )
    print(e)
    # yester_exchange = ExchangeRate.objects.filter(
    #     currency__icontains=currency, created_at__date=yester_day
    # ).last()

    # today_exchange = ExchangeRate.objects.filter(
    #     currency__icontains=currency, created_at__date=yester_day
    # ).last()

    # print(yester_exchange)
    # print(today_exchange)

from datetime import date, timedelta, datetime
from venv import create
from channels.db import database_sync_to_async
from django.core.cache import cache

from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate
YesterExchanteRate = ExchangeRate
LastExchanteRate = ExchangeRate


def date_offset(date: date, offset: int) -> date:
    return date - timedelta(days=offset)


def _work_date(date: date) -> date:
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


@database_sync_to_async
def fluctuation_rate(currency) -> tuple[YesterExchanteRate, LastExchanteRate]:
    today = _work_date(date=date.today())
    yester_day = _work_date(date=today - timedelta(1))

    yester_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=yester_day
    ).last()
    
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=today
    ).last()

    return (yester_exchange, today_exchange)


@database_sync_to_async
def closing_price(date: date, currency: str) -> ExchangeRate:
    date = _work_date(date)
    return ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=date
    ).last()

from datetime import date, timedelta, datetime
from channels.db import database_sync_to_async

from ..base import work_date
from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate
YesterExchanteRate = ExchangeRate
LastExchanteRate = ExchangeRate


@database_sync_to_async
def latest_exchange_aggregate(currency: str) -> tuple[MinExchanteRate, MaxExchanteRate]:
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=work_date(datetime.today())
    )
    return (
        today_exchange.order_by("standard_price")[0],
        today_exchange.order_by("-standard_price")[0],
    )


@database_sync_to_async
def latest_exchange(*args, **kwargs) -> list[ExchangeRate]:
    kwargs["created_at__date"] = work_date(datetime.today())
    return list(ExchangeRate.objects.filter(*args, **kwargs))


@database_sync_to_async
def fluctuation_rate(currency) -> tuple[YesterExchanteRate, LastExchanteRate]:
    today = work_date(datetime.today())
    yester_day = work_date(today - timedelta(1))

    yester_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=yester_day
    ).last()

    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=today
    ).last()

    return yester_exchange, today_exchange


@database_sync_to_async
def closing_price(currency: str) -> ExchangeRate:
    created = work_date(datetime.today() - timedelta(1))
    return ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=created
    ).last()

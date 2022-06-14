from channels.db import database_sync_to_async
from datetime import date, timedelta

from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate
FirstExchanteRate = ExchangeRate
LastExchanteRate = ExchangeRate


def _latest_date() -> date:
    today = date.today()
    offset = today.weekday() - 4
    if 0 < offset:
        return today - timedelta(days=offset)
    return today


@database_sync_to_async
def latest_exchange_aggregate(currency: str) -> tuple[MinExchanteRate, MaxExchanteRate]:
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=_latest_date()
    )
    return (
        today_exchange.order_by("standard_price")[0],
        today_exchange.order_by("-standard_price")[0]
    )


@database_sync_to_async
def latest_exchange(*args, **kwargs) -> list[ExchangeRate]:
    kwargs["created_at__date"] = _latest_date()
    # kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))

# fluctuation_rate()
# 어제 종가 / 현제가 * 100

@database_sync_to_async
def first_and_last_exchange(*args, **kwargs) -> tuple[FirstExchanteRate, LastExchanteRate]:
    kwargs["created_at__date"] = _latest_date()
    e = list(ExchangeRate.objects.filter(*args, **kwargs))
    return (e[0], e[-1])


@database_sync_to_async
def first_exchange(*args, **kwargs) -> ExchangeRate:
    kwargs["created_at__date"] = _latest_date()
    return ExchangeRate.objects.filter(*args, **kwargs).first()


@database_sync_to_async
def last_exchange(*args, **kwargs) -> ExchangeRate:
    kwargs["created_at__date"] = _latest_date()
    return ExchangeRate.objects.filter(*args, **kwargs).last()
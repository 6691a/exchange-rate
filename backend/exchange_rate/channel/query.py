from channels.db import database_sync_to_async
from datetime import date, timedelta

from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate


def latest_date() -> date:
    today = date.today()
    offset = today.weekday() - 4
    if 0 < offset:
        return today - timedelta(days=offset)
    return today


@database_sync_to_async
def latest_exchange_aggregate(currency: str) -> tuple[MinExchanteRate, MaxExchanteRate]:
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=latest_date()
        # currency__icontains=currency, created_at__date=date.today()
    )
    return (
        today_exchange.order_by("standard_price")[0],
        today_exchange.order_by("-standard_price")[0]
    )


@database_sync_to_async
def latest_exchange(*args, **kwargs) -> list[ExchangeRate]:
    kwargs["created_at__date"] = latest_date()
    # kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))
from datetime import date
from channels.db import database_sync_to_async

from ..models import ExchangeRate


MaxExchanteRate = ExchangeRate
MinExchanteRate = ExchangeRate



@database_sync_to_async
def today_exchange_aggregate(currency: str) -> tuple[MinExchanteRate, MaxExchanteRate, ]:
    today_exchange = ExchangeRate.objects.filter(
        currency__icontains=currency, created_at__date=date.today()
    )
    return (
        today_exchange.order_by("standard_price")[0],
        today_exchange.order_by("-standard_price")[0]
    )


@database_sync_to_async
def today_exchange(*args, **kwargs) -> list[ExchangeRate]:
    kwargs["created_at__date"] = date.today()
    return list(ExchangeRate.objects.filter(*args, **kwargs))
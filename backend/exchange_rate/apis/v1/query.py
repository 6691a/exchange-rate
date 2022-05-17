from asgiref.sync import sync_to_async
from django.db.models import Max, Min, F
from datetime import date
from django.db.models.query import QuerySet

from ...models import ExchangeRate


@sync_to_async
def today_exchange_aggregate(currency: str) -> QuerySet:
    return (
        ExchangeRate.objects.filter(
            currency__icontains=currency, created_at__date=date.today()
            # currency__icontains=currency, created_at__date="2022-05-13"
        )
        .aggregate(
            hight_price=Max(F("standard_price")), low_price=Min(F("standard_price"))
        )
    )


@sync_to_async
def today_exchange(currency: str) -> list[ExchangeRate]:
    return list(
        # ExchangeRate.objects.filter(currency__icontains=currency, created_at__date="2022-05-13")
        ExchangeRate.objects.filter(currency__icontains=currency, created_at__date=date.today())
    )

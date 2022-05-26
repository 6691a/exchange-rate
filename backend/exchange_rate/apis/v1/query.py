from asgiref.sync import sync_to_async
from datetime import date

from ...models import ExchangeRate


@sync_to_async
def today_exchange(currency: str) -> list[ExchangeRate]:
    if not currency: 
        return

    return list(
        # ExchangeRate.objects.filter(currency__icontains=currency, created_at__date="2022-05-13")
        ExchangeRate.objects.filter(currency__icontains=currency, created_at__date=date.today())
    )

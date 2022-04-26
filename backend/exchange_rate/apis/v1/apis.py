from urllib import response
from ninja import Router
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet

from ...models import ExchangeRate
from .schemas import ExchangeRateSchema

router = Router()

@sync_to_async
def _exchange_latest(latest: str, *args, **kwargs) -> QuerySet | None:
    try:
        return ExchangeRate.objects.filter(*args, **kwargs).latest(latest)
    except ExchangeRate.DoesNotExist:
        return None


@router.get("", response={200: ExchangeRateSchema})
async def get_exchange_rate(request, currency: str):
    test = await _exchange_latest("created_at", currency__icontains=currency)
    print(test.__dict__)
    return test

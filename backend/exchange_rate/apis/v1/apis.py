from ninja import Router
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet

from base.schemas import ErrorSchema
from ...models import ExchangeRate
from .schemas import ExchangeRateSchema

router = Router()

@sync_to_async
def _exchange_latest(latest: str, *args, **kwargs) -> QuerySet | None:
    try:
        return ExchangeRate.objects.filter(*args, **kwargs).latest(latest)
    except ExchangeRate.DoesNotExist:
        return None


@router.get("", response={200: ExchangeRateSchema, 400: ErrorSchema})
async def get_exchange_rate(request, currency: str):
    exchange = await _exchange_latest("created_at", currency__icontains=currency)
    if not exchange:
            return 400, ErrorSchema(error="currency not found").dict()
    return 200, exchange

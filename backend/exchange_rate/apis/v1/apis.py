from ninja import Router
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet

from base.schemas import ResponseSchema, ErrorSchema

from ...models import ExchangeRate
from .schemas import ExchangeRateSchema

router = Router()


@sync_to_async
def _exchange_latest(latest: str, *args, **kwargs) -> QuerySet | None:
    try:
        return ExchangeRate.objects.filter(*args, **kwargs).latest(latest)
    except ExchangeRate.DoesNotExist:
        return None


@router.get(
    "", response={200: ResponseSchema[ExchangeRateSchema], 400: ResponseSchema[ErrorSchema]}
)
async def get_exchange_rate(request, currency: str):
    exchange = await _exchange_latest("created_at", currency__icontains=currency)
    if not exchange:
        return 400, ResponseSchema(data=ErrorSchema(error="currency not found"), status=400)

    return 200, ResponseSchema(data=ExchangeRateSchema(**exchange.dict))


# from datetime import date
# from typing import List


# @sync_to_async
# def today_exchange(*args, **kwargs):
#     kwargs["created_at__date"] = date.today()
#     return list(ExchangeRate.objects.filter(*args, **kwargs))


# @router.get("")
# async def test(request):
#     data = await today_exchange()
#     list[ExchangeRateSchema(data=data)]
#     return 200

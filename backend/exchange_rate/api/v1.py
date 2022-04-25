from ninja import Router
from typing import Union
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet

from ..models import ExchangeRate

router = Router()


@sync_to_async
def _exchange_latest(latest: str, *args, **kwargs) -> Union[QuerySet, None]:
    try:
        return ExchangeRate.objects.filter(*args, **kwargs).latest(latest)
    except ExchangeRate.DoesNotExist:
        return None


@router.get("")
async def get_exchange_rate(request, currency: str):
    test = await _exchange_latest("created_at", currency__icontains=currency)
    print(test)
    return {"message": "Hello from V1"}

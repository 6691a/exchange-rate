from ninja import Router
from asgiref.sync import sync_to_async

from ...models import ExchangeRate
from .schemas import ExchangeRateSchema
router = Router()


# def _():

@router.get("", response=list[ExchangeRateSchema])
async def get_exchange_rate(request, currency: str):
    test = await sync_to_async(list)(ExchangeRate.objects.filter(currency__icontains=currency))
    return test
    # return {"message": "Hello from V1"}

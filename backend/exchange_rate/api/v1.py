from ninja import Router
from asgiref.sync import sync_to_async

from ..models import ExchangeRate
router = Router()


@router.get('')
async def get_exchange_rate(request, currency: str):
    test = await sync_to_async(list)(ExchangeRate.objects.latest(currency__icontains=currency))
    print(test)
    return {'message': 'Hello from V1'}
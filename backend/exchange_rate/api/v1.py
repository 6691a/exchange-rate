from ninja import Router
from ..models import ExchangeRate
router = Router()

@router.get('/')
def get_exchange_rate(request, currency: str):
    return {'message': 'Hello from V1'}
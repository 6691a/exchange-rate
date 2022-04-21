from ninja import Router
from pkg_resources import to_filename
from ..models import ExchangeRate, ExchangeRateSchedule
from django.core.cache import cache
from datetime import datetime

router = Router()


@router.get("/")
def get_exchange_rate(request, currency: str):
    return {"message": "Hello from V1"}

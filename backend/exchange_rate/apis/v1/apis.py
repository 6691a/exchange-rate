from calendar import c
from base.schemas import ErrorSchema, ResponseSchema
from ninja import Router

from .schemas import ExchangeRateSchema, ChartSchema
from datetime import date, timedelta, datetime

router = Router()

from channel.base import channel_group_send
from asgiref.sync import async_to_sync
from ...models import ExchangeRate
from django.utils import timezone


@router.get("test/")
def test(request):
    return 200

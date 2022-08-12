from ninja import Router

from django.http import HttpRequest

from exchange_rate.base import work_date
from exchange_rate.models import ExchangeRateSchedule
from datetime import date
router = Router()


@router.get("test")
def test(request: HttpRequest):
    work_date(date(2022, 8, 15))

    return 200
    # ExchangeRateSchedule.objects.filter(day_off__range=[])
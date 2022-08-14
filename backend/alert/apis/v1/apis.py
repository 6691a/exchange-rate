from ninja import Router
from ninja.security import django_auth

from django.http import HttpRequest

from exchange_rate.base import work_date
from exchange_rate.models import ExchangeRateSchedule
from datetime import date

from alert.apis.v1.schemas import AlertCreateSchema

router = Router()


@router.post("/")
def test(request: HttpRequest, body: AlertCreateSchema):
    print(body)

    return 200

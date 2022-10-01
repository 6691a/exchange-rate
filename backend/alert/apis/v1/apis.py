import datetime

from ninja import Router

from django.http import HttpRequest
from asgiref.sync import async_to_sync

from exchange_rate.caches import country_cache, exchange_cache
from alert.apis.v1.schemas import AlertCreateSchema, AlertDeleteSchema
from alert.models import Alert
from exchange_rate.channel.schemas import ExchangeRateSchema


router = Router()


@router.get("/")
def get_alert(request: HttpRequest):
    return 200


@router.post(
    "/",
    response={200: None, 404: None}
)
def add_alert(request: HttpRequest, body: AlertCreateSchema):
    country = country_cache(body.currency)
    # 알림 설정 이상, 이하 체크
    if exchange := async_to_sync(exchange_cache)(body.currency):
        if exchange[-1].standard_price - body.price > 0:
            range = Alert.RANGE_CHOICE[1][0]
        else:
            range = Alert.RANGE_CHOICE[0][0]

    Alert.objects.get_or_create(
        price=body.price,
        user=request.user,
        country=country,
        range=range
    )
    return 200


@router.delete(
    "/",
    response={204: None, 404: None}
)
def del_alert(request: HttpRequest, body: AlertDeleteSchema):
    country = country_cache(body.currency)
    alert = Alert.objects.find_not_send(request.user, country)
    alert.delete()
    return 204, None


# alert kakao talk test api
# @router.get("/test/")
# def test(request, price: int):
#     from exchange_rate.models import ExchangeRate
#     obj = ExchangeRate.objects.create(
#         fix_time=datetime.date.today(),
#         currency="USD",
#         country="미국",
#         standard_price=price,
#     )
#     from exchange_rate.tasks import send_alert
#     send_alert(obj)
#     return 200

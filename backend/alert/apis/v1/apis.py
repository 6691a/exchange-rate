from ninja import Router

from django.http import HttpRequest

from exchange_rate.caches import country_cache
from alert.apis.v1.schemas import AlertCreateSchema
from alert.models import Alert
from exchange_rate.models import Country
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
    Alert.objects.get_or_create(
        price=body.price,
        user=request.user,
        country=country,
        active=True,
    )

    return 200

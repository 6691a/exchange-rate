from ninja import Router
from django.forms.models import model_to_dict
from django.conf import settings

from account.models import WatchList
from base.utils import cache_model
from base.schemas import ErrorSchema, ResponseSchema
from .schemas import CountrySchema, WatchListSchema
from exchange_rate.models import Country

# from account.tasks import insert_watch_list, delete_watch_list

router = Router()


@router.get(
    "watch", response={200: ResponseSchema[list[CountrySchema]], 400: ResponseSchema[ErrorSchema]}
)
def get_watch_list(request):
    watch_list = WatchList.objects.filter(user=request.user).select_related("country")

    if not watch_list:
        return 400, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=400)

    return 200, ResponseSchema(data=[CountrySchema(**model_to_dict(i.country)) for i in watch_list])


@router.post("watch", response={200: None, 404: ResponseSchema[ErrorSchema]})
def add_watch_list(request, watch: WatchListSchema):
    # 30일 캐싱
    country = cache_model(
        Country, watch.currency, settings.THIRTY_DAY_TO_SECOND, currency=watch.currency
    )
    if not WatchList.objects.get_or_create(user=request.user, country=country):
        return 404, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=404)

    # insert_watch_list.delay(user_id=request.user.id, country_id=country.id)
    return 200, None


@router.delete("watch")
def delete_watch_list(request, watch: WatchListSchema):
    ...

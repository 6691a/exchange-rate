from ninja import Router
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.conf import settings

from account.models import WatchList
from base.schemas import ErrorSchema, ResponseSchema
from .schemas import CountrySchema, WatchListSchema
from ...base import cache_country
from account.tasks import insert_watch_list

router = Router()


@router.get(
    "watch", response={200: ResponseSchema[list[CountrySchema]], 400: ResponseSchema[ErrorSchema]}
)
def get_watch_list(request):
    watch_list = WatchList.objects.filter(user=request.user).select_related("country")
    # watch_list = WatchList.objects.filter(user_id=4).select_related("country")

    if not watch_list:
        return 400, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=400)

    return 200, ResponseSchema(data=[CountrySchema(**model_to_dict(i.country)) for i in watch_list])


@router.post("watch")
def add_watch_list(request, watch: WatchListSchema):

    # 30일 캐싱
    country = cache_country(watch.currency, settings.THIRTY_DAY_TO_SECOND, currency=watch.currency)
    # celery로 db insert 넘김
    # insert_watch_list.delay(user_id=request.user.id, country_id=country.id)
    insert_watch_list.delay(user_id=1, country_id=country.id)

    return 200


#     watch = watch.dict()
#     print(watch)
#     print(request.user)
#     # user = request.user
#     return 200


@router.delete("watch")
def delete_watch_list(request):
    ...

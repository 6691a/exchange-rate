from asgiref.sync import async_to_sync

from ninja import Router

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from exchange_rate.models import WatchList
from base.schemas import ErrorSchema, ResponseSchema
from .schemas import CountrySchema, WatchListSchema
from exchange_rate.models import Country
from exchange_rate.caches import country_cache, exchange_cache

router = Router()


@router.get("/")
def get_exchange_list(request: HttpRequest, currency: str):
    data = async_to_sync(exchange_cache)(currency)
    return 200

@router.get(
    "watch/",
    response={200: ResponseSchema[list[CountrySchema]], 400: ResponseSchema[ErrorSchema]},
)
def get_watch_list(request: HttpRequest):
    watch_list: WatchList = WatchList.objects.filter(user=request.user).select_related("country")

    if not watch_list:
        return 400, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=400)

    return 200, ResponseSchema(data=[CountrySchema(**model_to_dict(i.country)) for i in watch_list])


@router.post(
    "watch/",
    response={200: None, 404: ResponseSchema[ErrorSchema]},
)
def add_watch_list(request: HttpRequest, watch: WatchListSchema):
    # 30일 캐싱
    country = country_cache(watch.currency)
    if not WatchList.objects.get_or_create(user=request.user, country=country):
        return 404, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=404)

    return 200, None


@router.delete(
    "watch/",
    response={204: None, 404: None},
)
def delete_watch_list(request: HttpRequest, watch: WatchListSchema):
    # 30일 캐싱
    country = country_cache(watch.currency)
    watch_list = get_object_or_404(WatchList, user=request.user, country=country)
    watch_list.delete()
    return 204, None


@router.get(
    "country/",
    response={200: ResponseSchema[list[CountrySchema]]}
)
def get_country_list(request: HttpRequest):
    return 200, ResponseSchema(data=[CountrySchema(**model_to_dict(i)) for i in Country.objects.all()])
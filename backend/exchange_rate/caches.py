from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .channel.query import latest_exchange
from .models import Country


def country_cache(currency: str) -> Country:
    key = f"country_{currency}"
    if country := cache.get(key):
        return country
    country = get_object_or_404(Country, currency=currency)
    cache.set(key, country, settings.THIRTY_DAY_TO_SECOND)
    return country


async def exchange_cache(currency: str):
    # exchange_rate.task에도 이름 변경
    key = f"{settings.CACHE_KEY_EXCHANGE}{currency}"
    if exchange := cache.get(key):
        return exchange
    exchange = await latest_exchange(currency__icontains=currency)
    cache.set(key, exchange)
    return exchange



from django.core.cache import cache
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async, async_to_sync

from .models import Country


async def async_cache_county(key: str, timeout: int = 300, **kwargs) -> Country:
    key = f"county_{key}"

    if county := cache.get(key):
        return county

    country = await sync_to_async(get_object_or_404)(Country, **kwargs)
    cache.set(key, country, timeout)
    return country


def cache_country(key: str, timeout: int = 300, **kwargs) -> Country:
    return async_to_sync(async_cache_county)(key, timeout, **kwargs)

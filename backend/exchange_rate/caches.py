from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import Country


def country_cache(currency: str) -> Country:
    if not (country := cache.get(f"country_{currency}")):
        country = get_object_or_404(Country, currency=currency)
        cache.set(
            f"country_{currency}",
            country,
            timeout=None
        )
    return country

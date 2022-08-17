from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from exchange_rate.caches import country_cache
from exchange_rate.models import Country

@login_required
def alert(request, currency):
    country: Country = country_cache(currency)
    print(country)
    context: dict = {
        "country": country,
    }
    return render(request, "alert.html", context)


def alert_beat(request, currency):
    country: Country = country_cache(currency)
    context = {
        country: country
    }
    return render(request, "alert_beat.html", context)


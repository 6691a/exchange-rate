from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .caches import country_cache
from .models import Country
from alert.models import Alert
from exchange_rate.models import WatchList
from account.models import User

# @login_required
def main(request):
    context = {}
    if request.user.is_authenticated:
        user: User = request.user
        context = {"watchList": WatchList.objects.filter(user=user).select_related("country")}
    return render(request, "main.html", context)


# @login_required
def currency(request, currency):
    country: Country = country_cache(currency)
    context = {}

    if request.user.is_authenticated:
        user: User = request.user
        alert: Alert = Alert.objects.get_object_or_none(user=request.user, country=country, active=True, send=False)
        context: dict = {
            "country": country,
            "watch": False,
            "alert": alert
        }
        if WatchList.objects.filter(user=user, country=country).exists():
            context["watch"] = True

    return render(request, "currency.html", context)



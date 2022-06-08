from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Country
from account.models import WatchList


@login_required
def main(request):
    user = request.user
    context = {
        "watchList": WatchList.objects.filter(user=user).select_related("country")
    }
    return render(request, "main.html", context)


@login_required
def exchange_rate(request, currency):
    user = request.user
    country = get_object_or_404(Country, currency__icontains=currency)

    context = {
        "country": country,
        "watch": False
    }
    if WatchList.objects.filter(user=user, currency__icontains=currency).exists():
        context["watch"] = True

    return render(request, "exchange_rate.html", context)


@login_required
def exchange(reqeust, currency):
    ...
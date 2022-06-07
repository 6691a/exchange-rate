from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Country
from account.models import WatchList

def main(request):
    return redirect('exchange_rate:main', "usd")

@login_required
def exchange_rate(request, currency):
    user = request.user
    country = get_object_or_404(Country, currency__icontains=currency)

    context = {
        "country": country,
        "watch": False
    }

    if WatchList.objects.exclude(user=user, currency=currency):
        context["watch"] = True

    return render(request, "exchange_rate.html", context)


# @login_required
def test(request):
    return render(request, "test.html")


@login_required
def exchange(reqeust, currency):
    ...
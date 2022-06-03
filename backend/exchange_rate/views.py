from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Country
from django.shortcuts import redirect

def main(request):
    return redirect('exchange_rate:main', "usd")

# @login_required
def exchange_rate(request, currency):
    # print(Country.objects.get(country=currency))
    context = {"currency": currency}

    return render(request, "exchange_rate.html", context)


# @login_required
def test(request):
    return render(request, "test.html")


@login_required
def exchange(reqeust, currency):
    ...
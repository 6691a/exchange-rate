from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Country

def main(request):
    return render(request, "exchange_rate.html")

# @login_required
def exchange_rate(request, currency):
    print(Country.objects.get(currency__icontains=currency))
    context = {"currency": currency}

    return render(request, "exchange_rate.html", context)


# @login_required
def test(request):
    return render(request, "test.html")


@login_required
def exchange(reqeust, currency):
    ...
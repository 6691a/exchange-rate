from django.shortcuts import redirect


def main():
    return redirect("exchange_rate:main")


def login():
    return redirect("account:login")


def logout():
    return redirect("account:logout")

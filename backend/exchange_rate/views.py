from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def main(request):
    return render(request, "main.html")


def index(request):
    return render(request, "room.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})

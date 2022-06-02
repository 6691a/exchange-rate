from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# @login_required
def main(request):
    return render(request, "main.html")

def test(request):
    return render(request, "test.html")

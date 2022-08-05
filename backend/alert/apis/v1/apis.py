from ninja import Router

from django.http import HttpRequest

router = Router()


@router.get("test")
def test(request: HttpRequest):
    ...
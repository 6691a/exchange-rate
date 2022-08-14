from ninja import Router

from django.http import HttpRequest

from alert.apis.v1.schemas import AlertCreateSchema
from alert.models import Alert

router = Router()


@router.get("/")
def get_alert(request: HttpRequest):
    return 200


@router.post("/")
def add_alert(request: HttpRequest, body: AlertCreateSchema):
    print(body)

    return 200

from ninja import Router
from ninja.security import django_auth

from .schemas import WatchListSchema

router = Router()

@router.get("watch")
def get_like(request):
    ...



@router.post("watch")
def create_like(request, watch: WatchListSchema):
    watch = watch.dict()
    print(watch)
    print(request.user)
    # user = request.user
    return 200


# @router.delete("watch/{id}")
# def delete_like(request):
#     return 200
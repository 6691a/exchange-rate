from ninja import Router
from ninja.security import django_auth
from asgiref.sync import sync_to_async

from .schemas import WatchListSchema
from .query import watch_list_query
router = Router()


@router.get("watch", auth=django_auth)
async def get_like(request):
    a = sync_to_async(request.auth)()
    print(a)
    # print(request.user)
    # watch_list = await watch_list_query(request.user)
    # print(watch_list)
    return 201


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
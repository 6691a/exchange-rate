from ninja import Router
from django.forms.models import model_to_dict

from account.models import WatchList
from base.schemas import ErrorSchema, ResponseSchema
from .schemas import CountrySchema
router = Router()


# @router.get("watch", response={200: ResponseSchema[CountrySchema]})
@router.get("watch")
def get_like(request):
    watch_list = WatchList.objects.filter(user_id=4).select_related("country")
    return 200, ResponseSchema(
        data=[CountrySchema(**model_to_dict(i.country)) for i in watch_list]
    )


# @router.post("watch")
# def create_like(request, watch: WatchListSchema):
#     watch = watch.dict()
#     print(watch)
#     print(request.user)
#     # user = request.user
#     return 200


# @router.delete("watch/{id}")
# def delete_like(request):
#     return 200
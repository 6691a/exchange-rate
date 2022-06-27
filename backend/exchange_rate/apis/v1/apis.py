from ninja import Router
from django.forms.models import model_to_dict

from account.models import WatchList
from base.schemas import ErrorSchema, ResponseSchema
from .schemas import CountrySchema

router = Router()


@router.get(
    "watch", response={200: ResponseSchema[list[CountrySchema]], 400: ResponseSchema[ErrorSchema]}
)
# @router.get("watch")
def get_watch_list(request):
    # watch_list = WatchList.objects.filter(user=request.user).select_related("country")
    watch_list = WatchList.objects.filter(user_id=4).select_related("country")

    if not watch_list:
        return 400, ResponseSchema(data=ErrorSchema(error="watch list not found"), status=400)

    return 200, ResponseSchema(data=[CountrySchema(**model_to_dict(i.country)) for i in watch_list])


# @router.get("",
# async def today_exchange_rate(request, currency: str):
#     if exchange := await today_exchange(currency):
#         aggregate = await today_exchange_aggregate(currency)
#         return 200, ResponseSchema(
#             data=ChartSchema(
#                 exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
#                 **aggregate,
#             )
#         )
#


# @router.post("watch")
# def set_like(request, watch: WatchListSchema):
#     watch = watch.dict()
#     print(watch)
#     print(request.user)
#     # user = request.user
#     return 200


# @router.delete("watch/{id}")
# def delete_like(request):
#     return 200

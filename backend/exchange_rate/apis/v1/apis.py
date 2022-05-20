from base.schemas import ErrorSchema, ResponseSchema
from ninja import Router

from .schemas import ExchangeRateSchema, ChartSchema
from .query import today_exchange_aggregate, today_exchange

router = Router()


@router.get(
    "", response={200: ResponseSchema[ChartSchema], 400: ResponseSchema[ErrorSchema]}
)
async def today_exchange_rate(request, currency: str):
    if exchange := await today_exchange(currency):
        aggregate = await today_exchange_aggregate(currency)
        return 200, ResponseSchema(
            data=ChartSchema(
                exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
                **aggregate,
            )
        )
    return 400, ResponseSchema(data=ErrorSchema(error="currency not found"), status=400)
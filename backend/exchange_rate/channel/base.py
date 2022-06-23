from base.schemas import ResponseSchema
from .schemas import ExchangeRateSchema, ChartSchema
from .query import latest_exchange_aggregate, closing_price
from ..models import ExchangeRate

Json = str


async def exchange_rate_msg(exchange: list[ExchangeRate] | ExchangeRate, currency: str) -> Json:
    low, high = await latest_exchange_aggregate(currency=currency)
    closing = await closing_price(currency=currency)
    if not isinstance(exchange, list):
        exchange = [exchange]

    return ResponseSchema(
        data=ChartSchema(
            exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
            hight_price=ExchangeRateSchema(**high.dict),
            low_price=ExchangeRateSchema(**low.dict),
            closing_price=ExchangeRateSchema(**closing.dict),
        ),
    ).json()

from base.schemas import ResponseSchema
from .exceptions import ClosingPriceException, FluctuationException
from .schemas import ExchangeRateSchema, ChartSchema, WatchListSchema
from .query import latest_exchange_aggregate, closing_price, fluctuation_rate
from ..models import ExchangeRate

Json = str


async def exchange_rate_msg(exchange: list[ExchangeRate] | ExchangeRate, currency: str) -> Json:
    low, high = await latest_exchange_aggregate(currency=currency)
    closing = await closing_price(currency=currency)

    if not isinstance(exchange, list):
        exchange = [exchange]

    if not closing:
        raise ClosingPriceException

    return ResponseSchema(
        data=ChartSchema(
            exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
            hight_price=ExchangeRateSchema(**high.dict),
            low_price=ExchangeRateSchema(**low.dict),
            closing_price=ExchangeRateSchema(**closing.dict),
        ),
    ).json()


async def watch_msg(currency: str) -> Json:
    yester, last = await fluctuation_rate(currency)

    if not yester or not last:
        raise FluctuationException

    return ResponseSchema(
        data=WatchListSchema(yester_exchange=yester, last_exchange=last)
    ).json()





from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from .schemas import ExchangeRateSchema, ChartSchema, WatchListSchema
from .query import latest_exchange, latest_exchange_aggregate, first_and_last_exchange, fluctuation_rate


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        currency = self.group_name
        if exchange := await latest_exchange(currency__icontains=currency):
            low, high = await latest_exchange_aggregate(currency=currency)
            return await self.send(
                ResponseSchema(
                    data=ChartSchema(
                        exchange_rate=[ExchangeRateSchema(**i.dict) for i in exchange],
                        hight_price=ExchangeRateSchema(**high.dict),
                        low_price=ExchangeRateSchema(**low.dict)
                    ),
                ).json()
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        super().disconnect(close_code)


class WatchListConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        currency = self.group_name
        await fluctuation_rate(currency)
        # first, last = await first_and_last_exchange(currency__icontains=currency)
        # if first and last:
        #     return await self.send(
        #         ResponseSchema(
        #             data=WatchListSchema(
        #                 first_exchange=first,
        #                 last_exchange=last
        #             )
        #         ).json()
        #     )
        # await self.send(
        #     ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        # )
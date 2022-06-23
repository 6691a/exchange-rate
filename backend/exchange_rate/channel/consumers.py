from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from .schemas import ExchangeRateSchema, ChartSchema, WatchListSchema
from .query import latest_exchange, latest_exchange_aggregate, fluctuation_rate, closing_price
from .base import exchange_rate_msg


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        currency = self.group_name
        if exchange := await latest_exchange(currency__icontains=currency):
            return await self.send(
                await exchange_rate_msg(exchange, currency)
            )
        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

    async def disconnect(self, close_code):
        await super().disconnect(close_code)


class WatchListConsumer(BaseWebSocket):
    async def connect(self):
        await super().connect()
        currency = self.group_name
        yester, last = await fluctuation_rate(currency)
        if yester and last:
            return await self.send(
                ResponseSchema(
                    data=WatchListSchema(yester_exchange=yester, last_exchange=last)
                ).json()
            )

        await self.send(
            ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
        )

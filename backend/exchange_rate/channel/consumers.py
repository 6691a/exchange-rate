from base.schemas import ResponseSchema, ErrorSchema

from channel.base import BaseWebSocket
from exchange_rate.caches import exchange_cache
from .messages import exchange_rate_msg, watch_msg
from .exceptions import ClosingPriceException, FluctuationException


class ExchangeRateConsumer(BaseWebSocket):
    async def connect(self):
        currency = self.scope["url_route"]["kwargs"]["currency"].upper()
        group_name = currency
        await super().connect(group_name=group_name)
        try:
            if exchange := await exchange_cache(currency):
                return await self.send(await exchange_rate_msg(exchange, currency))
        except ClosingPriceException:
            await self.send(
                ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
            )

    async def disconnect(self, close_code):
        await super().disconnect(close_code)


class WatchListConsumer(BaseWebSocket):
    async def connect(self):
        currency = self.scope["url_route"]["kwargs"]["currency"].upper()
        await super().connect(f'watch_{currency}')

        try:
            return await self.send(await watch_msg(currency))
        except FluctuationException:
            await self.send(
                ResponseSchema(data=ErrorSchema(error="currency not found"), status=400).json()
            )

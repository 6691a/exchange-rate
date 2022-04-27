from venv import create
from ...models import ExchangeRate
from base.schemas import BaseSchema
from datetime import datetime


class ExchangeRateSchema(BaseSchema):
    currency: str
    sales_rate: str
    fix_time: str
    created_at: str

    @staticmethod
    def resolve_currency(obj):
        currency = obj.currency.split()
        return f"{currency[0]}"

    @staticmethod
    def resolve_fix_time(obj):
        return obj.fix_time.strftime("%Y.%m.%d %H:%M")
    
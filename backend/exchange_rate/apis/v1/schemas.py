from ninja import Schema
from typing import Optional

class ExchangeRateSchema(Schema):
    currency: Optional[str]
    sales_rate: float

    @staticmethod
    def resolve_currency(obj):
        print(obj.currency)
        return "1"
from ninja import ModelSchema
from ...models import ExchangeRate


class ExchangeRateSchema(ModelSchema):
    @staticmethod
    def resolve_currency(obj):
        print(obj.currency)
        return f"{obj.currency}12312312312"

    class Config:
        model = ExchangeRate
        model_fields = ["currency", "sales_rate", "fix_time", "created_at"]

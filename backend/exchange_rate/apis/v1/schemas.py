from datetime import datetime
from base.schemas import BaseSchema

from pydantic import validator


class ExchangeRateSchema(BaseSchema):
    country: str
    currency: str
    standard_price: float
    fix_time: datetime
    created_at: datetime

    @validator("fix_time")
    def validate_fix_time(cls, v):
        return cls.kst_time(v)


class ChartSchema(BaseSchema):
    exchange_rate: list[ExchangeRateSchema]
    # hight_price: ExchangeRateSchema
    # low_price: ExchangeRateSchema

    hight_price: ExchangeRateSchema | None
    low_price: ExchangeRateSchema | None
    chart_length: int = 79

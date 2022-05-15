from datetime import datetime
from base.schemas import BaseSchema

from pydantic import validator


class ExchangeRateSchema(BaseSchema):
    currency: str
    standard_price: float
    fix_time: datetime
    created_at: datetime

    @validator("currency")
    def validate_currency(cls, v):
        return v.split()[0]

    @validator("fix_time")
    def validate_fix_time(cls, v):
        return cls.kst_time(v)


class ChartSchema(BaseSchema):
    exchange_rate: list[ExchangeRateSchema]
    hight_price: float | None
    low_price: float | None

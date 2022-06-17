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
    hight_price: ExchangeRateSchema 
    low_price: ExchangeRateSchema 
    chart_length: int = 60


class WatchListSchema(BaseSchema):
    yester_exchange: ExchangeRateSchema
    last_exchange: ExchangeRateSchema
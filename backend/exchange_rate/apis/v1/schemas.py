from datetime import datetime
from base.schemas import BaseSchema

from pydantic import validator


class ExchangeRateSchema(BaseSchema):
    currency: str
    sales_rate: str
    fix_time: datetime
    created_at: datetime

    @validator("currency")
    def validate_currency(cls, v):
        return v.split()[0]

    @validator("fix_time")
    def validate_fix_time(cls, v):
        return cls.kst_time(v)

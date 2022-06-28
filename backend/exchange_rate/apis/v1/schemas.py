from datetime import datetime
from base.schemas import BaseSchema
from pydantic import validator
from ninja import Schema


class CountrySchema(BaseSchema):
    currency: str
    name: str
    currency_kr: str
    standard_price: float


class WatchListSchema(BaseSchema):
    currency: str

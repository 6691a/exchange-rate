from datetime import datetime
from base.schemas import BaseSchema

from pydantic.generics import GenericModel 
from pydantic import validator
from typing import TypeVar, Generic

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    data: T
    status: int = 200

    # @validator('status', always=True, allow_reuse=True)
    # def validate_status(cls, v, values):
    #     print(cls, v, values)
    #     return v
    # def __new__(cls, data: BaseModel, schema: Schema):
    #     if not isinstance(data, BaseModel):
    #         raise TypeError("data is not `BaseModel` instance")

    #     if not issubclass(schema, Schema):
    #         raise TypeError("schema is not django-ninja `Schema` instance")

    #     model_data = data.model_to_dict
    #     return schema(**model_data)


class ExchangeRateSchema(BaseSchema):
    currency: str
    sales_rate: str
    fix_time: datetime
    created_at: datetime

    @validator('currency')
    def validate_currency(cls, v):
        print(v.split()[0])
        return v.split()[0]

    @validator('fix_time')
    def validate_fix_time(cls, v):
        return v.strftime("%Y.%m.%d %H:%M")

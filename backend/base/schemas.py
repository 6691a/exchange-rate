from datetime import datetime
from ninja import Schema
from typing import TypeVar, Generic
from pydantic.generics import GenericModel
from pydantic import validator
from django.conf import settings

T = TypeVar("T")


class ResponseSchema(GenericModel, Generic[T]):
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


class ErrorSchema(Schema):
    error: str


class BaseSchema(Schema):
    @classmethod
    def kst_time(cls, time: datetime):
        return time.astimezone().strftime(settings.DATE_TIME_FORMATE)

    @validator("created_at", check_fields=False)
    def validate_created_at(cls, v):
        return cls.kst_time(v)

    @validator("updated_at", check_fields=False)
    def validate_updated_at(cls, v):
        return cls.kst_time(v)

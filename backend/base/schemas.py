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

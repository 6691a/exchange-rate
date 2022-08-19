from pydantic import validator

from ninja import Schema

from base.schemas import BaseSchema


class AlertDeleteSchema(BaseSchema):
    currency: str


class AlertCreateSchema(AlertDeleteSchema):
    price: int



from pydantic import validator

from ninja import Schema

from base.schemas import BaseSchema


class AlertCreateSchema(BaseSchema):
    currency: str
    price: int


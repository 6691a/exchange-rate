from ninja import Schema
from typing import TypeVar, Generic
from pydantic.generics import GenericModel

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
    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.strftime("%Y.%m.%d %H:%M")

    @staticmethod
    def resolve_updated_at(obj):
        return obj.updated_at.strftime("%Y.%m.%d %H:%M")

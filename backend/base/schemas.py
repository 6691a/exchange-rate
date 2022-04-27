from ninja import Schema
from pydantic import create_model

class ErrorSchema(Schema):
    error: str


class BaseSchema(Schema):
    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.strftime("%Y.%m.%d %H:%M")

    @staticmethod
    def resolve_updated_at(obj):
        return obj.updated_at.strftime("%Y.%m.%d %H:%M")
    
    class Config:
        schema_extra = {
            "data": dict,
            "status": int
        }

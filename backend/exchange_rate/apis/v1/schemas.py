from ninja import Schema, ModelSchema
from typing import Optional
from ...models import ExchangeRate

# class ExchangeRateSchema(ModelSchema):
#     currency: str

#     @staticmethod
#     def resolve_owner(obj):
#         print(obj)
#         return f"1`2312312312"

#     class Config:
#         model = ExchangeRate
#         model_fields = ["currency", "sales_rate", "fix_time", "created_at"]

class ExchangeRateSchema(Schema):
    currency: str
    owner: str
    @staticmethod
    def resolve_owner(obj):
        print("123123")
        return f"123"

class TaskSchema(Schema):
    id: int
  
    
    currency: Optional[str]
    lower_title: str

    @staticmethod
    def resolve_currency(obj):
        return f"{obj.currency} {obj.currency}"

    def resolve_lower_title(self, obj):
        return self.title.lower()
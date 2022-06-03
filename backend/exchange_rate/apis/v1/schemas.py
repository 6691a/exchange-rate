from datetime import datetime
from base.schemas import BaseSchema
from pydantic import validator

class WatchListSchema(BaseSchema):
    currency: str
    
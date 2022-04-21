from ninja import NinjaAPI
from exchange_rate.api.v1 import router as exchange_rate_router

api = NinjaAPI(title="Exchange_rate", version='1.0.0')

api.add_router("v1/", exchange_rate_router)
from ninja import NinjaAPI
from django.conf import settings

from exchange_rate.apis.v1.apis import router as exchange_rate_router

docs_url = ""

if settings.DEBUG:
    docs_url = "/docs"

# api = NinjaAPI(title="Exchange_rate", version='1.0.0', docs_url=docs_url, renderer=Response())
api = NinjaAPI(title="Exchange_rate", version="1.0.0", docs_url=docs_url)


api.add_router("v1/", exchange_rate_router, tags=["exchange_rate"])

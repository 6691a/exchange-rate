from ninja import NinjaAPI
from ninja.security import django_auth

from django.conf import settings

from exchange_rate.apis.v1.apis import router as exchange_rate_router
from alert.apis.v1.apis import router as alert_router

docs_url = ""

if settings.DEBUG:
    docs_url = "/docs"

# api = NinjaAPI(title="Exchange_rate", version='1.0.0', docs_url=docs_url, renderer=Response())
api = NinjaAPI(title="Exchange_rate", version="1.0.0", docs_url=docs_url, csrf=True, auth=django_auth)


api.add_router("v1/", exchange_rate_router, tags=["exchange_rate"])
api.add_router("v1/alert", alert_router, tags=["alert"])

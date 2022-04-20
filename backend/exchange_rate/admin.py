from django.contrib import admin

from .models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass
    list_display = ["call_date", "currency", "sales_rate",]
    # search_fields = ["id", "username", "company_code__company_code"]
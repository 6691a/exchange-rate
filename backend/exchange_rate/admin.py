from django.contrib import admin

from .models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass
    list_display = ["currency", "sales_rate", "fix_time", "created_at"]
    # search_fields = ["id", "username", "company_code__company_code"]
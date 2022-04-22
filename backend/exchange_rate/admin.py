from django.contrib import admin

from .models import ExchangeRate, ExchangeRateSchedule

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["currency", "sales_rate", "fix_time", "created_at"]
    # search_fields = ["id", "username", "company_code__company_code"]

@admin.register(ExchangeRateSchedule)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["day_off", "memo"]
    # search_fields = ["id", "username", "company_code__company_code"]
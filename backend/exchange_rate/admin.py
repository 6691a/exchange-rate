from django.contrib import admin

from .models import ExchangeRate, ExchangeRateSchedule, Country


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["country", "currency", "standard_price", "created_at", "fix_time"]
    # search_fields = ["id", "username", "company_code__company_code"]


@admin.register(ExchangeRateSchedule)
class ExchangeRateScheduleAdmin(admin.ModelAdmin):
    list_display = ["day_off", "memo"]
    # search_fields = ["id", "username", "company_code__company_code"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "currency", "currency_kr", "standard_price"]
    # search_fields = ["id", "username", "company_code__company_code"]

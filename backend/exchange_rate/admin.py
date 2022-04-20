from django.contrib import admin

from .models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass
    # list_display = ["id", "username", "company", "first_name", "is_joined"]
    # search_fields = ["id", "username", "company_code__company_code"]
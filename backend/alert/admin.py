from django.contrib import admin

from .models import Alert, Alert_beat


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["country", "price", "send", "range"]

@admin.register(Alert_beat)
class AlertBeatAdmin(admin.ModelAdmin):
    ...
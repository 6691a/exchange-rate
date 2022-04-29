from django.contrib import admin

from .models import User


@admin.register(User)
class EUserAdmin(admin.ModelAdmin):
    list_display = ["email", "nickname", "gender", "age_range"]
    search_fields = ["email", "nickname", "gender"]

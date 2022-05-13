from django.contrib import admin

from .models import User, Setting


class SeetingInline(admin.TabularInline):
    model = Setting
    can_delete = False
    verbose_name_plural = 'setting'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "nickname", "gender", "age_range"]
    search_fields = ["email", "nickname", "gender"]
    # inlines = (SeetingInline, )
    
   

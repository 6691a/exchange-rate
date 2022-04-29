from django.apps import AppConfig


# class AccountConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'account'

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    label = 'any_unique_name'
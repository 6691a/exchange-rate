# Generated by Django 4.0.4 on 2022-06-07 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0002_rename_name_country_currency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='country',
            new_name='name',
        ),
    ]

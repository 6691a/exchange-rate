# Generated by Django 4.0.4 on 2022-06-08 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_alter_watchlist_currency"),
    ]

    operations = [
        migrations.RenameField(
            model_name="watchlist",
            old_name="currency",
            new_name="country",
        ),
    ]

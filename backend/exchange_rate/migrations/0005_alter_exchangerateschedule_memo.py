# Generated by Django 3.2.13 on 2022-04-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_rate", "0004_exchangerateschedule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangerateschedule",
            name="memo",
            field=models.TextField(blank=True, null=True, verbose_name="메모"),
        ),
    ]

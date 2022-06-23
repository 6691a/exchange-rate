# Generated by Django 3.2.13 on 2022-05-02 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_rate", "0007_auto_20220426_1006"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangerate",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="생성일"
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="fix_time",
            field=models.DateTimeField(verbose_name="환율 갱신일"),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="수정일"),
        ),
        migrations.AlterField(
            model_name="exchangerateschedule",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="생성일"
            ),
        ),
        migrations.AlterField(
            model_name="exchangerateschedule",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="수정일"),
        ),
    ]

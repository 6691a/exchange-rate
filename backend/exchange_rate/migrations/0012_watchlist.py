# Generated by Django 4.0.4 on 2022-06-03 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exchange_rate", "0011_alter_exchangerate_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="WatchList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="생성일"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, null=True, verbose_name="수정일"),
                ),
                ("currency", models.CharField(max_length=10, verbose_name="통화")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watch_list",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="사용자",
                    ),
                ),
            ],
            options={
                "db_table": "watch_list",
                "ordering": [],
            },
        ),
    ]

# Generated by Django 3.2.13 on 2022-06-03 12:41

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [
        ("exchange_rate", "0001_initial"),
        ("exchange_rate", "0002_exchangerate_call_date"),
        ("exchange_rate", "0003_auto_20220421_0938"),
        ("exchange_rate", "0004_exchangerateschedule"),
        ("exchange_rate", "0005_alter_exchangerateschedule_memo"),
        ("exchange_rate", "0006_auto_20220423_1944"),
        ("exchange_rate", "0007_auto_20220426_1006"),
        ("exchange_rate", "0008_auto_20220502_2139"),
        ("exchange_rate", "0009_rename_sales_rate_exchangerate_standard_price"),
        ("exchange_rate", "0010_exchangerate_country_alter_exchangerate_currency"),
        ("exchange_rate", "0011_alter_exchangerate_options"),
        ("exchange_rate", "0012_watchlist"),
        ("exchange_rate", "0013_exchangeratelist"),
        ("exchange_rate", "0014_delete_watchlist"),
        ("exchange_rate", "0015_alter_exchangeratelist_country_and_more"),
        ("exchange_rate", "0016_alter_exchangeratelist_table"),
        ("exchange_rate", "0017_exchangeratelist_currency_kr_and_more"),
        ("exchange_rate", "0018_rename_currency_exchangeratelist_name_and_more"),
        ("exchange_rate", "0019_rename_exchangeratelist_country"),
        ("exchange_rate", "0020_auto_20220603_2134"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeRate",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("currency", models.CharField(max_length=25, verbose_name="통화")),
                (
                    "sales_rate",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="매매 기준"
                    ),
                ),
                (
                    "fix_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="환율 갱신 시간"
                    ),
                ),
            ],
            options={
                "db_table": "exchange_rate",
                "ordering": [],
            },
        ),
        migrations.CreateModel(
            name="ExchangeRateSchedule",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("day_off", models.DateField(verbose_name="쉬는 날")),
                ("memo", models.TextField(blank=True, null=True, verbose_name="메모")),
            ],
            options={
                "db_table": "exchange_rate_schedule",
                "ordering": [],
            },
        ),
        migrations.AlterModelManagers(
            name="exchangerate",
            managers=[],
        ),
        migrations.AlterModelManagers(
            name="exchangerateschedule",
            managers=[],
        ),
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
        migrations.RenameField(
            model_name="exchangerate",
            old_name="sales_rate",
            new_name="standard_price",
        ),
        migrations.AddField(
            model_name="exchangerate",
            name="country",
            field=models.CharField(default="None", max_length=25, verbose_name="국가"),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="currency",
            field=models.CharField(default="None", max_length=25, verbose_name="통화명"),
        ),
        migrations.AlterModelOptions(
            name="exchangerate",
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="ExchangeRateList",
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
                ("country", models.CharField(max_length=25, verbose_name="국가")),
                ("currency", models.CharField(max_length=25, verbose_name="통화명")),
            ],
            options={
                "db_table": "ExchangeRateList",
            },
        ),
        migrations.AlterModelTable(
            name="exchangeratelist",
            table="exchangeRateList",
        ),
        migrations.RenameField(
            model_name="exchangeratelist",
            old_name="currency",
            new_name="name",
        ),
        migrations.AddField(
            model_name="exchangeratelist",
            name="name_kr",
            field=models.CharField(
                default="null", max_length=25, verbose_name="한글 통화명"
            ),
        ),
        migrations.AddField(
            model_name="exchangeratelist",
            name="standard_price",
            field=models.DecimalField(
                decimal_places=2, default="1", max_digits=10, verbose_name="매매 기준"
            ),
        ),
        migrations.AlterModelTable(
            name="exchangeratelist",
            table="country",
        ),
        migrations.RenameModel(
            old_name="ExchangeRateList",
            new_name="Country",
        ),
        migrations.AlterField(
            model_name="country",
            name="name",
            field=models.CharField(max_length=25, verbose_name="통화 단위"),
        ),
        migrations.AlterField(
            model_name="country",
            name="name_kr",
            field=models.CharField(
                default="null", max_length=25, verbose_name="한글 통화 단위"
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="currency",
            field=models.CharField(default="None", max_length=25, verbose_name="통화 단위"),
        ),
    ]

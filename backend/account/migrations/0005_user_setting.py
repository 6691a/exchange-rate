# Generated by Django 3.2.13 on 2022-05-15 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_setting"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="setting",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.setting",
            ),
        ),
    ]

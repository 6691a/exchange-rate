# Generated by Django 3.2.13 on 2022-05-15 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='setting',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.setting'),
        ),
    ]

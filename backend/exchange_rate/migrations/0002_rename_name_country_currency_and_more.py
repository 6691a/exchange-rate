# Generated by Django 4.0.4 on 2022-06-07 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0001_squashed_0020_auto_20220603_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='name',
            new_name='currency',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='name_kr',
            new_name='currency_kr',
        ),
    ]

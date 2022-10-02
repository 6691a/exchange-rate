# Generated by Django 4.0.5 on 2022-08-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='range',
            field=models.CharField(choices=[('More than', '이상'), ('Less than', '이하')], default='More than', max_length=10),
            preserve_default=False,
        ),
    ]
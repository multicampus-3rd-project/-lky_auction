# Generated by Django 3.0.5 on 2020-11-05 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20201105_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 8, 10, 4, 53, 146208)),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 5, 10, 4, 53, 146208)),
        ),
    ]
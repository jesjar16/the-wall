# Generated by Django 3.2.4 on 2021-07-08 01:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]

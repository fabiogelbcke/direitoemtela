# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-11 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_auto_20180211_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='one_time_use',
            field=models.BooleanField(default=True),
        ),
    ]

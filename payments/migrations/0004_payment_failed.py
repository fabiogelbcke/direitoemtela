# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 00:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20170502_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='failed',
            field=models.BooleanField(default=False),
        ),
    ]

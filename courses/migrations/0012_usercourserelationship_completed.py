# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20170331_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourserelationship',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
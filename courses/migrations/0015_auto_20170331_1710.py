# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20170331_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourserelationship',
            name='completion_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='usercourserelationship',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 01:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0032_auto_20170515_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='completion_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
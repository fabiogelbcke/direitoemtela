# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20170327_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseitem',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-06 16:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0037_auto_20170909_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='trailer_url',
            new_name='trailer_id',
        ),
    ]

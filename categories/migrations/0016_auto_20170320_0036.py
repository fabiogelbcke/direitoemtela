# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 00:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0015_category_hidden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videocategory',
            options={'ordering': ('position',)},
        ),
    ]

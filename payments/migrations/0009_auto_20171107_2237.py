# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-07 22:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20171107_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billinginfo',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_info', to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_auto_20161012_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='yt_id',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]

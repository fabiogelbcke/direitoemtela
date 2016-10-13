# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_videos'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='yd_id',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]

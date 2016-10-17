# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0012_auto_20161013_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocategory',
            name='yt_position',
            field=models.CharField(max_length=4, blank=True),
        ),
    ]

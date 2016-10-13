# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20161008_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='yt_id',
            field=models.TextField(max_length=20, blank=True),
        ),
    ]

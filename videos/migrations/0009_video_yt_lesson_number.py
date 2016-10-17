# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20161012_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='yt_lesson_number',
            field=models.CharField(max_length=4, blank=True),
        ),
    ]

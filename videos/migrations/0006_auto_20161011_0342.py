# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20161010_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='yt_title',
            field=models.CharField(max_length=300, blank=True),
        ),
    ]

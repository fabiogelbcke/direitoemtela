# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20161008_0129'),
        ('categories', '0002_auto_20160918_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='videos',
            field=models.ManyToManyField(related_name='categories', through='categories.VideoCategory', to='videos.Video'),
        ),
    ]

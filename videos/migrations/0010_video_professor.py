# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0013_videocategory_yt_position'),
        ('videos', '0009_video_yt_lesson_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='professor',
            field=models.ForeignKey(related_name='videos', to='categories.Professor', null=True),
        ),
    ]

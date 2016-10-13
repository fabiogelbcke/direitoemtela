# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import image_cropping.fields
import videos.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='video',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='video',
            name='published_at_yt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=image_cropping.fields.ImageCropField(default=b'logodefault.png', upload_to=videos.models.get_thumbnail_path, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name=b'thumbnail_ratio',
            field=image_cropping.fields.ImageRatioField(b'thumbnail', '854x480', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='thumbnail ratio'),
        ),
        migrations.AddField(
            model_name='video',
            name='yt_title',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]

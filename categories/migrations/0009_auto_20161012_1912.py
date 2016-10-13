# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields
import categories.models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_auto_20161012_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=image_cropping.fields.ImageCropField(default=b'logodefault.png', upload_to=categories.models.get_thumbnail_path, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name=b'thumbnail_ratio',
            field=image_cropping.fields.ImageRatioField(b'thumbnail', '1600x900', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='thumbnail ratio'),
        ),
    ]

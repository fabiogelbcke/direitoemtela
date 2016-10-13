# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161011_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name=b'thumbnail_ratio',
            field=image_cropping.fields.ImageRatioField(b'thumbnail', '1600x900', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='thumbnail ratio'),
        ),
    ]

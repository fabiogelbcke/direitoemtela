# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0009_auto_20161012_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name=b'thumbnail_ratio',
            field=image_cropping.fields.ImageRatioField(b'thumbnail', '592x300', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='thumbnail ratio'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 17:08
from __future__ import unicode_literals

import courses.models
from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_course_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='thumbnail',
            field=image_cropping.fields.ImageCropField(blank=True, default='logodefault.png', upload_to=courses.models.get_thumbnail_path),
        ),
        migrations.AddField(
            model_name='course',
            name='thumbnail_ratio',
            field=image_cropping.fields.ImageRatioField('thumbnail', '592x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='thumbnail ratio'),
        ),
    ]
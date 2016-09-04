# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields
import categories.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('description', models.TextField(blank=True)),
                ('profile_image', image_cropping.fields.ImageCropField(default=b'logodefault.png', upload_to=categories.models.get_image_path, blank=True)),
                (b'profile_ratio', image_cropping.fields.ImageRatioField(b'profile_image', '320x320', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='profile ratio')),
            ],
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('category', models.ForeignKey(to='categories.Category')),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
        ),
    ]

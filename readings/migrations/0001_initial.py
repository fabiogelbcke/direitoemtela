# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import readings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_file', models.FileField(blank=True, default='', upload_to=readings.models.get_reading_path, validators=[readings.models.validate_reading_format])),
                ('description', models.TextField(blank=True, default='')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]

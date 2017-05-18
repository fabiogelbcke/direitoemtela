# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-02 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_courseitem_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseitem',
            name='video',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_items', to='videos.Video'),
        ),
    ]

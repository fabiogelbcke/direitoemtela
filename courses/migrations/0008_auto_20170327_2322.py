# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 23:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170327_2321'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseTopics',
            new_name='CourseTopic',
        ),
    ]

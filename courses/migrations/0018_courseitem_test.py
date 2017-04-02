# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-02 02:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursetests', '0002_auto_20170402_0256'),
        ('courses', '0017_course_total_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseitem',
            name='test',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='coursetests.CourseTest'),
        ),
    ]

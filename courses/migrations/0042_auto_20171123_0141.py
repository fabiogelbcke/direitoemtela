# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-23 01:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0041_auto_20171123_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourserelationship',
            name='certificate',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_rel', to='courses.Certificate'),
        ),
    ]

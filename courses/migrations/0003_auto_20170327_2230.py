# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='professor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='categories.Professor'),
        ),
    ]

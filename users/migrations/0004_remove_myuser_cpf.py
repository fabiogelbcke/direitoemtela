# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_myuser_course_hours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='cpf',
        ),
    ]

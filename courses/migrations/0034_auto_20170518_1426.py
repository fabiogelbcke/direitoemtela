# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0033_certificate_completion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='users.MyUser'),
        ),
        migrations.AlterField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(related_name='courses', through='courses.UserCourseRelationship', to='users.MyUser'),
        ),
        migrations.AlterField(
            model_name='courseitem',
            name='users',
            field=models.ManyToManyField(related_name='course_items', through='courses.UserItemRelationship', to='users.MyUser'),
        ),
        migrations.AlterField(
            model_name='usercourserelationship',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MyUser'),
        ),
        migrations.AlterField(
            model_name='useritemrelationship',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MyUser'),
        ),
    ]

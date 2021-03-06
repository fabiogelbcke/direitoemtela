# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 23:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_professor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTopics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='courses.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='learningpoints',
            name='course',
        ),
        migrations.DeleteModel(
            name='LearningPoints',
        ),
    ]

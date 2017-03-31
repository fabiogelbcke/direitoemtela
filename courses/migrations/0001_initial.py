# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('videos', '0010_video_professor'),
        ('categories', '0016_auto_20170320_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('trailer_url', models.CharField(blank=True, default='', max_length=300)),
                ('hidden', models.BooleanField(default=False)),
                ('professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='categories.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='CourseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('item_type', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='courses.Course')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_items', to='videos.Video')),
            ],
        ),
        migrations.CreateModel(
            name='LearningPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_points', to='courses.Course')),
            ],
        ),
    ]
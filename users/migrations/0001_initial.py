# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(default=users.models.generate_username, max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=80)),
                ('cpf', models.CharField(blank=True, max_length=14)),
                ('profile_image', image_cropping.fields.ImageCropField(blank=True, default='logodefault.png', upload_to=users.models.get_image_path)),
                ('profile_ratio', image_cropping.fields.ImageRatioField('profile_image', '320x320', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='profile ratio')),
                ('email_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

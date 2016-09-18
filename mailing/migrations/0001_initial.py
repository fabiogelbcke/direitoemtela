# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailingEmail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

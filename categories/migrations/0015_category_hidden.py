# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0014_auto_20161019_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]

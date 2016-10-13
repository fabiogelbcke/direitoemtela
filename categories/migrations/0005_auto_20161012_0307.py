# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_category_yd_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='yd_id',
            new_name='yt_id',
        ),
    ]

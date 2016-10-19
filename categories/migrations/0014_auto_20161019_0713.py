# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0013_videocategory_yt_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='professor',
            field=models.ForeignKey(related_name='categories', blank=True, to='categories.Professor', null=True),
        ),
    ]

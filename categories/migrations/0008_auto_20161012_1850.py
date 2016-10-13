# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20161012_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='professor',
            field=models.ForeignKey(related_name='categories', to='categories.Professor', null=True),
        ),
    ]

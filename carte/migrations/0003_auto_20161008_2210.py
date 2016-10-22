# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0002_auto_20161008_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(default='chilly food', max_length=100),
        ),
    ]

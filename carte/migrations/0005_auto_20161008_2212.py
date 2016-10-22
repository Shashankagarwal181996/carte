# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0004_auto_20161008_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0006_auto_20161008_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(upload_to=b''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(upload_to=b''),
        ),
    ]

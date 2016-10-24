# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0009_auto_20161023_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='url',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 23, 53, 39, 665570, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='url',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 23, 53, 49, 372224, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

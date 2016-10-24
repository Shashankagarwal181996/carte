# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0008_auto_20161019_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='review',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='review',
        ),
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 12, 49, 39, 932902, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_tags',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 12, 50, 0, 5821, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='rate_review',
            field=models.ManyToManyField(to='carte.Rate_Review', blank=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cuisines',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 12, 50, 2, 178608, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='description',
            field=models.TextField(default=datetime.datetime(2016, 10, 23, 12, 50, 7, 28326, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

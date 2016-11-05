# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0018_auto_20161104_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate_review',
            name='user_profile',
            field=models.ForeignKey(default=1, to='carte.Profile'),
        ),
    ]

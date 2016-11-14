# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0019_rate_review_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='menu',
            field=models.ImageField(default='/home/shashank/Downloads/kolkata/shrizmenu1.jpg', upload_to=b''),
        ),
    ]

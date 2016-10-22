# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='tags',
        ),
        migrations.AddField(
            model_name='hotel',
            name='tag',
            field=models.ManyToManyField(to='carte.Tags'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tag',
            field=models.ManyToManyField(to='carte.Tags'),
        ),
    ]

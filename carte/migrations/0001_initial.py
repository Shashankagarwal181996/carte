# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('location', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('tags', models.TextField()),
                ('rating', models.FloatField()),
                ('review', models.TextField()),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('location', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('tags', models.TextField()),
                ('rating', models.FloatField()),
                ('review', models.TextField()),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
    ]

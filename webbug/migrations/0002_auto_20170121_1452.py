# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbug', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hit',
            name='real_ip',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hit',
            name='remote_port',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-08-07 02:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180802_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
    ]

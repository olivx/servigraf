# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-23 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_auto_20170822_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor'),
        ),
    ]

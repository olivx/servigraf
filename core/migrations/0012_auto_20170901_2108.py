# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-01 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170901_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='documento',
            field=models.CharField(blank=True, max_length=30, verbose_name='CNPJ'),
        ),
    ]
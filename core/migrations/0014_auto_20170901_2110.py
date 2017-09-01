# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-01 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170901_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contato',
            name='nome',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='contato',
            name='sobre_nome',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=70, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='logradouro',
            field=models.CharField(max_length=50, verbose_name='Logradouro'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-01 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170901_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='documento',
            field=models.CharField(blank=True, max_length=20, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.SmallIntegerField(choices=[(1, 'Juridico'), (2, 'Fisico')], default=1, verbose_name='Fisico/Juridico'),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='telefone',
            field=models.CharField(max_length=15, verbose_name='Telefone'),
        ),
    ]

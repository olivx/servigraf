# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-21 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170719_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefone',
            name='ddd',
        ),
        migrations.AlterField(
            model_name='telefone',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(9, 'OI'), (6, 'TIM'), (2, 'FAX'), (1, 'FIXO'), (8, 'VIVO'), (3, 'CASA'), (7, 'CLARO'), (5, 'CELULAR'), (4, 'TRABALHO')], default=1, verbose_name='Tipo'),
        ),
    ]
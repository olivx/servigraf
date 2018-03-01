# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-03-01 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_auto_20171124_1109'),
        ('project', '0007_auto_20180113_2310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectclient',
            options={'verbose_name': 'Projeto Cliente', 'verbose_name_plural': 'Projetos Clientes'},
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': 'Projeto', 'verbose_name_plural': 'Projetos'},
        ),
        migrations.AddField(
            model_name='projects',
            name='services',
            field=models.ManyToManyField(through='project.ProjectServices', to='catalogo.Produto'),
        ),
    ]
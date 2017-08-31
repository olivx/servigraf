# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-14 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoProduto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=50, verbose_name='Grupo')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('tipo', models.PositiveIntegerField(default=1, verbose_name='Tipo')),
                ('valor', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Valor')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observação')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('data_create', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('data_update', models.DateTimeField(auto_now=True, verbose_name='Alterado')),
                ('ativo', models.NullBooleanField(default=True)),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='catalogo.GrupoProduto')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'Produtos',
                'verbose_name': 'Produto',
            },
        ),
    ]

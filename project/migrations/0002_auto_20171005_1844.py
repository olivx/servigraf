# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-05 18:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20170901_2110'),
        ('catalogo', '0005_auto_20170901_1523'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
            ],
            options={
                'verbose_name_plural': 'Projetos Serviços',
                'verbose_name': 'Projeto Serviço',
            },
        ),
        migrations.CreateModel(
            name='ProjetoSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pi', models.CharField(max_length=20, verbose_name='PI')),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor Unitario')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Valor Unitario')),
                ('acabamento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Acabamento')),
                ('timestamp', models.DateField(verbose_name='Data pedido')),
                ('entrega', models.TimeField(verbose_name='Horario de Entrega')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observação')),
            ],
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': 'Projeto Cliente', 'verbose_name_plural': 'Projetos Clientes'},
        ),
        migrations.AddField(
            model_name='projects',
            name='clients',
            field=models.ManyToManyField(to='core.Cliente'),
        ),
        migrations.AddField(
            model_name='projetosales',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.AddField(
            model_name='projetosales',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectServices'),
        ),
        migrations.AddField(
            model_name='projetosales',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectservices',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects'),
        ),
        migrations.AddField(
            model_name='projectservices',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='catalogo.Produto'),
        ),
    ]
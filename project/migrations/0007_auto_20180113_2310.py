# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-01-13 23:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0006_auto_20171124_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='active',
            field=models.NullBooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='projects',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='projects',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
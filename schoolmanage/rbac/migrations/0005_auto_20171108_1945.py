# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_permission_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.group', verbose_name='所在分组'),
        ),
    ]

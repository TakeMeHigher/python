# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_permission_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='code',
            field=models.CharField(max_length=32, null=True, verbose_name='代码'),
        ),
    ]
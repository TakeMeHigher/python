# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20171103_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='sex',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10),
        ),
    ]

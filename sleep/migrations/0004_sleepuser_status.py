# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0003_auto_20171122_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='sleepuser',
            name='status',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6b63\u5728\u7761\u89c9'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-12 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_list_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='list',
            options={'ordering': ('-id',)},
        ),
    ]

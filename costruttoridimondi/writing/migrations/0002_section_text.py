# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
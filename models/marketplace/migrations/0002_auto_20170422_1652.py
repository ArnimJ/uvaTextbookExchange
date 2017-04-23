# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-22 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbookpost',
            name='textbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textbook', to='marketplace.Textbook'),
        ),
    ]

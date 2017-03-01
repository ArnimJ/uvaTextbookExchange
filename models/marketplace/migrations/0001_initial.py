# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-01 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=70)),
                ('isbn', models.BigIntegerField()),
                ('author', models.CharField(max_length=70)),
                ('publicationDate', models.DateField(blank=True, null=True)),
                ('publisher', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextbookPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('postTitle', models.CharField(max_length=70)),
                ('condition', models.CharField(max_length=70)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(max_length=70)),
                ('sold', models.BooleanField(default=False)),
                ('viewCount', models.IntegerField(default=0)),
                ('postDate', models.DateField(auto_now_add=True, null=True)),
                ('textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Textbook')),
            ],
        ),
    ]

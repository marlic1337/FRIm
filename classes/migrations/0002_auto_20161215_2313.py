# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predmet',
            fields=[
                ('predmet_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('predmet_name', models.CharField(max_length=100)),
                ('predmet_category', models.CharField(default=b'razno', max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Classes',
        ),
    ]
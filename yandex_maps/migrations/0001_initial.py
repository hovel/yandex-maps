# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapAndAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(db_index=True, max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name='\u0428\u0438\u0440\u043e\u0442\u0430', blank=True)),
            ],
        ),
    ]

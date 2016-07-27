# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('rent_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='use end time')),
            ],
        ),
    ]

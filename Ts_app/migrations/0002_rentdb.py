# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ts_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentDB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d_type', models.CharField(max_length=100)),
                ('d_id', models.IntegerField()),
                ('d_pic', models.ImageField(upload_to=b'')),
                ('p_name', models.CharField(max_length=100)),
            ],
        ),
    ]

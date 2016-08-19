# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RentDB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d_type', models.CharField(max_length=100)),
                ('d_id', models.CharField(max_length=100)),
                ('d_pic', models.ImageField(upload_to='img')),
                ('p_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestlinkCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_name', models.CharField(default='null', max_length=100, null=True, blank=True)),
                ('case_sum', models.TextField(null=True, blank=True)),
                ('case_step', models.TextField(max_length=4000, null=True, blank=True)),
                ('case_except', models.TextField(null=True, blank=True)),
                ('internalid', models.CharField(default='0000', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TestlinkDB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suite_name', models.CharField(max_length=100)),
                ('suite_detail', models.TextField()),
                ('suite_id', models.CharField(max_length=100)),
                ('parent_suite_name', models.ForeignKey(related_name='children', blank=True, to='Ts_app.TestlinkDB', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_name', models.CharField(max_length=1000)),
                ('user_name', models.CharField(max_length=100)),
                ('rent_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='use end time')),
            ],
        ),
        migrations.AddField(
            model_name='testlinkcase',
            name='case_suite',
            field=models.ForeignKey(related_name='children_case', blank=True, to='Ts_app.TestlinkDB', null=True),
        ),
    ]

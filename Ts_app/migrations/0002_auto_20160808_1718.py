# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ts_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testlinkcase',
            name='internalid',
            field=models.CharField(default='0000', max_length=1000),
        ),
    ]

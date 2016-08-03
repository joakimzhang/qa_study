# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ts_app', '0002_rentdb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentdb',
            name='d_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='rentdb',
            name='d_pic',
            field=models.CharField(max_length=100),
        ),
    ]

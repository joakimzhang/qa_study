# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ts_app', '0003_auto_20160729_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentdb',
            name='d_pic',
            field=models.ImageField(upload_to='img'),
        ),
    ]

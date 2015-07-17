# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20150717_0200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='delivery_fee',
        ),
    ]

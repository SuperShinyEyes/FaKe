# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0020_auto_20150723_0836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='donkey',
        ),
    ]

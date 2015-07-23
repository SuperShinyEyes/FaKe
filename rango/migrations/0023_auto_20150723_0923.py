# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0022_auto_20150723_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='goods',
            new_name='products',
        ),
    ]

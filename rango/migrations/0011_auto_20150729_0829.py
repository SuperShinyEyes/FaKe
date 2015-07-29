# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20150729_0756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('sold_amount', 'registeration_time'), 'permissions': (('can_sell', 'Can sell products. Thus he is a seller'),)},
        ),
    ]

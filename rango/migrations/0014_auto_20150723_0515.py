# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0013_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ('price',), 'permissions': (('can_sell', 'Can sell products. Thus he is a seller'),)},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': (('can_order', 'Can make and view orders'),)},
        ),
    ]

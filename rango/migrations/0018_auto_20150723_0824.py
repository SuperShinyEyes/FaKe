# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0017_auto_20150723_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(to='rango.Goods', null=True),
        ),
    ]

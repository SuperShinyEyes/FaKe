# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0016_auto_20150723_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='goods',
            name='cart',
            field=models.ForeignKey(to='rango.Cart', null=True),
        ),
    ]

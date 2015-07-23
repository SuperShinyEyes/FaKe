# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0021_remove_cart_donkey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='goods',
        ),
        migrations.AddField(
            model_name='cart',
            name='goods',
            field=models.ManyToManyField(to='rango.Goods'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_auto_20150722_0514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=1)),
                ('purchased_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.ForeignKey(to='rango.Member')),
                ('orders', models.ForeignKey(to='rango.Orders')),
                ('product', models.ForeignKey(to='rango.Goods')),
            ],
            options={
                'permissions': (('can_make_orders', 'Can make and view orders'),),
            },
        ),
    ]

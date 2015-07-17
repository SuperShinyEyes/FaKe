# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_auto_20150717_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=100)),
                ('registered_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('category_name',),
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('product_num', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('stock', models.IntegerField()),
                ('sold_amount', models.IntegerField()),
                ('expiration_date', models.DateTimeField()),
                ('delivery_fee', models.DecimalField(max_digits=6, decimal_places=2)),
                ('product_info', models.CharField(max_length=4000)),
                ('status', models.BooleanField()),
                ('due_date', models.DateTimeField()),
                ('registeration_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('categories', models.ManyToManyField(to='rango.Category')),
                ('sellers', models.ForeignKey(to='rango.Member')),
            ],
            options={
                'ordering': ('price',),
            },
        ),
    ]

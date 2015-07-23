# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0019_auto_20150723_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donkey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='donkey',
            field=models.ForeignKey(to='rango.Donkey', null=True),
        ),
    ]

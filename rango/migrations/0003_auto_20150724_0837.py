# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20150724_0621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='registered_time',
            new_name='registeration_time',
        ),
    ]

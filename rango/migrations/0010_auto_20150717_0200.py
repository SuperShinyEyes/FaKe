# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rango.models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0009_category_goods'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='sellers',
            new_name='seller',
        ),
        migrations.AddField(
            model_name='goods',
            name='edited_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='due_date',
            field=models.DateTimeField(default=rango.models.get_deadline),
        ),
        migrations.AlterField(
            model_name='goods',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='sold_amount',
            field=models.IntegerField(default=0),
        ),
    ]

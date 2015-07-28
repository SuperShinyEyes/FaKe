# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0004_auto_20150727_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited_time', models.DateTimeField(null=True, blank=True)),
                ('product', models.ForeignKey(to='rango.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited_time', models.DateTimeField(null=True, blank=True)),
                ('comment', models.ForeignKey(to='rango.Comment')),
                ('product', models.ForeignKey(to='rango.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

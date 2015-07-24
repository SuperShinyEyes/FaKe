# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rango.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
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
            name='Donkey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='OldProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('purchased_date', models.DateTimeField(null=True)),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_order', 'Can make and view orders'),),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('product_num', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('stock', models.IntegerField()),
                ('sold_amount', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('expiration_date', models.DateTimeField(null=True)),
                ('product_info', models.CharField(max_length=4000)),
                ('status', models.BooleanField()),
                ('due_date', models.DateTimeField(default=rango.models.get_deadline)),
                ('registeration_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited_time', models.DateTimeField(null=True, blank=True)),
                ('categories', models.ManyToManyField(to='rango.Category')),
                ('seller', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('price',),
                'permissions': (('can_sell', 'Can sell products. Thus he is a seller'),),
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('products', models.ManyToManyField(to='rango.Product')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_cls', models.CharField(default=b'2', max_length=1, choices=[(b'1', b'Seller'), (b'2', b'Buyer')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='rango.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='rango.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]

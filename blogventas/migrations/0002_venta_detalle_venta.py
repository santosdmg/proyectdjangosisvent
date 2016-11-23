# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='detalle_venta',
            field=models.ManyToManyField(null=True, blank=True, to='blogventas.Producto', through='blogventas.Detalle_venta'),
        ),
    ]

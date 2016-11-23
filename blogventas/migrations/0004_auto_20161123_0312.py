# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogventas', '0003_cliente_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_venta',
            name='cantidad',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='detalle_venta',
            name='subtotal',
            field=models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=18),
        ),
    ]

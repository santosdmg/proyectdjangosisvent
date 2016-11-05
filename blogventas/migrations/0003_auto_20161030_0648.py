# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogventas', '0002_producto_existencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='caracteristicas',
            field=models.TextField(),
        ),
    ]

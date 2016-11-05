# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('nit', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Detalle_venta',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(max_digits=18, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('modelo', models.CharField(max_length=30)),
                ('caracteristicas', models.CharField(max_length=50)),
                ('imagen', models.FileField(null=True, blank=True, upload_to='')),
                ('precio', models.DecimalField(max_digits=18, decimal_places=2)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogventas.Marca')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nro_factura', models.IntegerField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.DecimalField(max_digits=18, decimal_places=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogventas.Cliente')),
                ('detalle_venta', models.ManyToManyField(through='blogventas.Detalle_venta', null=True, blank=True, to='blogventas.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='detalle_venta',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_detalleventa_producto', to='blogventas.Producto'),
        ),
        migrations.AddField(
            model_name='detalle_venta',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_detalleventa_venta', to='blogventas.Venta'),
        ),
    ]

# -*- coding: utf8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib import admin

from django.utils import timezone

#PARA EL MODELO MARCA
class Marca(models.Model):
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return self.descripcion



#PARA EL MODELO CLIENTE
class Cliente(models.Model):
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    nit = models.CharField(max_length=11)
    direccion = models.CharField(max_length=11, null = True, blank = True)
    def __str__(self):
        return '%s' %(self.nombres+' '+self.apellidos)

#PARA EL MODELO PRODUCTO
class Producto(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    modelo = models.CharField(max_length=30)
    caracteristicas = models.TextField()
    imagen = models.FileField(null=True, blank=True)
    precio = models.DecimalField(max_digits=18, decimal_places=2)
    existencia = models.IntegerField( null= True, blank = True)
    def __str__(self):
        return '%s' %(self.modelo+' / Q.' +str(self.precio))

#PARA EL MODELO VENTA
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    nro_factura = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    detalle_venta = models.ManyToManyField(Producto, through='Detalle_venta', null=True, blank=True)
    def __str__(self):
        return '%s' %(self.nro_factura)

#PARA EL MODELO DETALLE
class Detalle_venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='fk_detalleventa_producto')
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name='fk_detalleventa_venta')
    cantidad = models.IntegerField( null=True, blank=True)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return '%s' %(self.cantidad)

class Detalle_ventaInLine(admin.TabularInline):
    model = Detalle_venta
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    inlines = (Detalle_ventaInLine,)

class VentaAdmin(admin.ModelAdmin):
    inlines = (Detalle_ventaInLine,)

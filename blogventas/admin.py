from django.contrib import admin
from .models import Marca, Cliente, Producto, Venta, Detalle_venta, ProductoAdmin, VentaAdmin


# Register your models here.
admin.site.register(Marca)
admin.site.register(Cliente)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Detalle_venta)

from django import forms
from .models import Producto, Marca, Venta
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm


class RegistrarUs(UserCreationForm):
    class Meta:
        model = User
        fields = [
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'user_permissions',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                    ]
    def __init__ (self, *args, **kwargs):
        super(RegistrarUs, self).__init__(*args, **kwargs)
        self.fields["user_permissions"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["user_permissions"].help_text = "Seleccionar los permisos"
        self.fields["user_permissions"].queryset = Permission.objects.all()

class ProductoN(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('marca', 'modelo', 'caracteristicas', 'precio','existencia','imagen', )

class frmMarca(forms.ModelForm):
    class Meta:
        model = Marca
        fields= ('descripcion',)

class frmVenta(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ('cliente','nro_factura', 'detalle_venta', 'total'  )
    def __init__ (self, *args, **kwargs):
        super (frmVenta, self).__init__(*args, **kwargs)
        self.fields['detalle_venta'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['detalle_venta'].help_text = "Seleccione los productos a comprar"
        self.fields['detalle_venta'].queryset = Producto.objects.all()

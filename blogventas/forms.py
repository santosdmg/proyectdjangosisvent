from django import forms
from .models import Producto, Marca
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

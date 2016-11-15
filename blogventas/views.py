from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from .models import Producto
from .forms import RegistrarUs, ProductoN, frmMarca
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

# Create your views here.

#Para regustrar los usuarios

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = RegistrarUs(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('blogventas.views.lista_producto')
    else:
        formulario = RegistrarUs()
    return render(request,'usuario/nuevo_usuario.html', {'formulario' : formulario})

#Para iniciar sesion
def login_usuario(request):
    if not request.user.is_anonymous():
        return redirect('blogproyect.views.lista_recetas')
    if request.method=='POST':
        formulariologin = AuthenticationForm(request.POST)
        if formulariologin.is_valid:
            username = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username = username, password= clave)
            if acceso is not None:
                if acceso.is_active:
                    if acceso.is_staff:
                        login(request, acceso)
                        return redirect('blogventas.views.lista_producto')
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Usuario esta activo, pero no tiene acceso a area de administrador')

                else:
                    messages.add_message(request, messages.SUCCESS, 'Usuario inactivo, consulte con el adminisrador')



            else:
                messages.add_message(request, messages.SUCCESS, 'Verifique su usuario o contraseña')
        else:
            messages.add_message(request, messages.SUCCESS, 'No hay acceso')
    else:
        formulariologin= AuthenticationForm()
    return render(request,'usuario/login.html', {'formulariologin' : formulariologin})

#cerrar sesion

def cerrar_sesion(request):
    logout(request)
    return redirect('blogventas.views.lista_producto')

#Nuevo Producto
def nuevo_producto(request):
    if request.method == "POST":
        form = ProductoN(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blogventas.views.lista_producto')
    else:
        form = ProductoN()
    return render(request,'blogventas/nuevo_producto.html', {'form' : form})

def nueva_marca(request):
    if request.method == "POST":
        formM = frmMarca(request.POST)
        if formM.is_valid():
            post = formM.save(commit=False)
            post.save()
    else:
        formM = frmMarca()
    return render(request,'blogventas/nuevo_producto.html', {'formM' : formM})






#Index del proyecto
def lista_producto(request):
    posts = Producto.objects.all
    return render(request, 'blogventas/lista_producto.html',{'posts': posts})


#detalle de cada post
def post_detail (request, pk):
    post = get_object_or_404(Producto, pk=pk)
    return render(request, 'blogventas/post_detail.html', {'post': post})

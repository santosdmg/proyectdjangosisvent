from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from .models import Producto, Cliente, Venta, Detalle_venta
from .forms import RegistrarUs, ProductoN, frmMarca, frmVenta
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core import serializers
import json

# Create your views here.

#Para regustrar los usuarios
#@login_required(login_url = '/usuario/login/')
@permission_required('auth.add_user', login_url = '/')
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
        return redirect('blogventas.views.lista_producto')
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
@login_required(login_url = '/usuario/login/')
def cerrar_sesion(request):
    logout(request)
    return redirect('blogventas.views.lista_producto')

#Nuevo Producto
@login_required(login_url = '/usuario/login/')
@permission_required('blogventas.add_producto', login_url = '/')
def nuevo_producto(request):
    if request.method == "POST":
        form = ProductoN(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blogventas.views.lista_producto')
    else:
        form = ProductoN()
    return render(request,'blogventas/nuevo_producto.html', {'form' : form})

#editar producto
@login_required(login_url = '/usuario/login/')
@permission_required('blogventas.change_producto', login_url = '/')
def post_edit(request, pk):
    post = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoN(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blogventas.views.post_detail', pk=post.pk)
    else:
        form = ProductoN(instance=post)
    return render(request, 'blogventas/post_edit.html', {'form': form})

#eliminar producto
@login_required(login_url = '/usuario/login/')
@permission_required('blogventas.delete_producto', login_url = '/')
def del_product(request, pk=None):
    instance = get_object_or_404(Producto, pk=pk)
    instance.delete()
    redirect('blogventas.views.lista_producto')
    return HttpResponseRedirect('/lista/productos')

#Ingreso de la marca
@login_required(login_url = '/usuario/login/')
@permission_required('blogventas.add_marca', login_url = '/')
def nueva_marca(request):
    if request.method == "POST":
        formM = frmMarca(request.POST)
        if formM.is_valid():
            post = formM.save(commit=False)
            post.save()
    else:
        formM = frmMarca()
    return render(request,'blogventas/nueva_marca.html', {'formM' : formM})


#venta
def venta_nueva(request, pk):
    post = get_object_or_404(Producto, pk=pk)
    return render(request, 'blogventas/nueva_venta.html',{'post': post})
    form = None
    if request.method == "POST":
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            
            if 'numero' not in proceso:
                msg = 'Ingrese numero de factura'
                raise Exception(msg)
            if 'idprod' not in proceso:
                msg = 'seleccione un producto'
                raise Exception(msg)
            if 'cantidad' not in proceso:
                msg = 'ingrese una cantidad'
                raise Exception(msg)
            if 'idprod' not in proceso:
                msg = 'seleccione un producto'
                raise Exception(msg)
            if 'clienProv' not in proceso:
                msg = 'El cliente no ha sido seleccionado'
                raise Exception(msg)
           
            crearfactura = Venta(
                cliente = Cliente.objects.get(id= proceso['clienProv']),
                nro_factura = proceso['numero'],
                total = proceso['total']
                )
            crearfactura.save()

            crearDetalle =  Detalle_venta(
                producto = Producto.objects.get(id = proceso['idprod']),
                venta =  crearfactura,
                cantidad = proceso['cantidad'],
                subtotal = proceso['subtotal']
                )
            crearDetalle.save()

            messages.success(
                request, 'La venta se ha realizado satisfactoriamente')
        except e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)

    return render(request, 'blogventas/nueva_venta.html', {'form' : form},  context_instance=RequestContext(request))

#buscar cliente
def buscarCliente(request):
    idCliente = request.GET.get('nit')
    cliente = Cliente.objects.filter(nit__contains=idCliente)
    data = serializers.serialize(
        'json', cliente, fields=('nit', 'nombres', 'apellidos', 'direccion'))
    return HttpResponse(data, content_type='application/json')


#venta normal
@login_required(login_url = '/usuario/login/')
@permission_required('blogventas.add_venta', login_url = '/')
def vent(request):
    if request.method == "POST":
        formM = frmVenta(request.POST)
        if formM.is_valid():
            venta = Venta.objects.create(cliente= formM.cleaned_data['cliente'],nro_factura=formM.cleaned_data['nro_factura'], total = formM.cleaned_data['total'])
            for producto_id in request.POST.getlist('detalle_venta'):
                det = Detalle_venta(producto_id= producto_id, venta_id=venta.id)
                det.save()
                messages.add_message(request, messages.SUCCESS, 'venta realizada Exitosamente')
                return redirect('blogventas.views.lista_producto')
    else:
        formM = frmVenta()
    return render(request,'blogventas/venta.html', {'formM' : formM})



#Index del proyecto
def lista_producto(request):
    posts = Producto.objects.all
    return render(request, 'blogventas/lista_producto.html',{'posts': posts})



#lista general de productos
@login_required(login_url = '/usuario/login/')
def lista_gen_producto(request):
    posts = Producto.objects.all
    return render(request, 'blogventas/productos.html',{'posts': posts})


#detalle de cada post
def post_detail (request, pk):
    post = get_object_or_404(Producto, pk=pk)
    return render(request, 'blogventas/post_detail.html', {'post': post})



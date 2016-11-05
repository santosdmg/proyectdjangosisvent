from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from .models import Producto
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404



#Index del proyecto
def lista_producto(request):
    posts = Producto.objects.all
    return render(request, 'blogventas/lista_producto.html',{'posts': posts})


#detalle de cada post
def post_detail (request, pk):
    post = get_object_or_404(Producto, pk=pk)
    return render(request, 'blogventas/post_detail.html', {'post': post})

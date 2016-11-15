from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    url(r'^$', views.lista_producto, name='inicio'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='detalle'),
    url(r'^Produto/nuevo/$', views.nuevo_producto, name='prodN'),
    url(r'^Marca/nuevo/$', views.nueva_marca, name='marcaN'),
    url(r'^usuario/nuevo/$', views.nuevo_usuario, name='crear_Us'),
    url(r'^usuario/login/$', views.login_usuario, name='login_Us'),
    url(r'^usuario/salir/$', views.cerrar_sesion, name='logout_Us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

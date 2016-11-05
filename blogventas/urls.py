from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    url(r'^$', views.lista_producto, name='inicio'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='detalle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

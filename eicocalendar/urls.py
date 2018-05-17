from django.conf.urls import url, include
from . import views

app_name = "calendario"

urlpatterns = [ 
                url(r'^$', views.viewCalendar, name='viewCalendar'),
                url(r'^calendario/siguientemes/$', views.obtenerSiguienteMes, name='obtenerSiguienteMes'),
                url(r'^calendario/anteriormes/$', views.obtenerAnteriorMes, name='obtenerAnteriorMes'),
                url(r'^calendario/eventosfecha/(?P<dia>[0-9]+)/(?P<mes>[0-9]+)/(?P<anio>[0-9]+)/$', views.obtenerEventosFecha, name='obtenerEventosFecha'),
                
                
                

            ]
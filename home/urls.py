from django.conf.urls import url, include
from . import views

app_name = "home"



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^solicitarUsuario/$', views.solicitarUsuario, name='solicitarUsuario'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^errorLogin/$', views.errorLogin, name='errorLogin'),
    url(r'^servicio$', views.viewService, name='viewService'),
    url(r'^interes$', views.viewInteres, name='viewInteres'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^admin/estadisticasVisitas/$', views.estadisticasVisitas, name='estadisticasVisitas'),
    url(r'^admin/estadisticasVisitasAux/$', views.estadisticasVisitasAux, name='estadisticasVisitasAux'),
    url(r'^admin/estadisticasReacciones/$', views.estadisticasReacciones, name='estadisticasReacciones'),
    url(r'^admin/estadisticasReaccionesAux/$', views.estadisticasReaccionesAux, name='estadisticasReaccionesAux'),
    url(r'^admin/agregarSitio$', views.agregarSitio, name='agregarSitio'),
    url(r'^admin/agregarServicio$', views.agregarServicio, name='agregarServicio'),
    url(r'^admin/agregarUsuarios$', views.agregarUsuarios, name='agregarUsuarios'),
    url(r'^admin/editar/(?P<id>[0-9]+)$', views.editarSitio, name='editarSitio'),
    url(r'^admin/editarAux/(?P<id>[0-9]+)$', views.editarSitioAux, name='editarSitioAux'),
    url(r'^admin/eliminar/(?P<id>[0-9]+)$', views.eliminarSitio, name='eliminarSitio'),
    url(r'^admin/eliminarAux/(?P<id>[0-9]+)$', views.eliminarSitioAux, name='eliminarSitioAux'),
    url(r'^admin/editarservicio/(?P<id>[0-9]+)$', views.editarServicio, name='editarServicio'),
    url(r'^admin/editarservicioAux/(?P<id>[0-9]+)$', views.editarServicioAux, name='editarServicioAux'),
    url(r'^admin/eliminarservicio/(?P<id>[0-9]+)$', views.eliminarServicio, name='eliminarServicio'),
    url(r'^admin/eliminarservicioAux/(?P<id>[0-9]+)$', views.eliminarServicioAux, name='eliminarServicioAux'),
    url(r'^admin/agregarEvento$', views.agregarEvento, name='agregarEvento'),
    url(r'^admin/editarEvento/(?P<id>[0-9]+)$', views.editarEvento, name='editarEvento'),
    url(r'^admin/editarEventoAux/(?P<id>[0-9]+)$', views.editarEventoAux, name='editarEventoAux'),
    url(r'^admin/eliminarevento/(?P<id>[0-9]+)$', views.eliminarEvento, name='eliminarEvento'),
    url(r'^admin/eliminareventoAux/(?P<id>[0-9]+)$', views.eliminarEventoAux, name='eliminarEventoAux'),

    
    ]


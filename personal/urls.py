from django.conf.urls import url, include
from . import views

app_name = "perfil"
urlpatterns = [ 
                url(r'^$', views.viewProfile, name='viewProfile'),
                url(r'ajeno/(?P<id>[0-9]+)$', views.viewProfileUser, name='viewProfileUser'),
                url(r'editarPerfil/$', views.editarPerfil, name='editarPerfil'),
                url(r'agregarExpecienciaOTrabajo/$', views.agregarExperienciaOTrabajo, name='agregarExperienciaOTrabajo'),
                url(r'agregarEducacion/$', views.agregarEducacion, name='agregarEducacion'),
                url(r'^editar/editarEducacion/(?P<id>[0-9]+)$', views.editarEducacion, name='editarEducacion'),
                url(r'^editar/editarEducacionAux/(?P<id>[0-9]+)$', views.editarEducacionAux, name='editarEducacionAux'),
                url(r'^eliminar/eliminarEducacion/(?P<id>[0-9]+)$', views.eliminarEducacion, name='eliminarEducacion'),
                url(r'^eliminar/eliminareducacionAux/(?P<id>[0-9]+)$', views.eliminarEducacionAux, name='eliminarEducacionAux'),
                url(r'^editar/editarExperiencia/(?P<id>[0-9]+)$', views.editarExperiencia, name='editarExperiencia'),
                url(r'^editar/editarExperienciaAux/(?P<id>[0-9]+)$', views.editarExperienciaAux, name='editarExperienciaAux'),
                url(r'^eliminar/eliminarExperiencia/(?P<id>[0-9]+)$', views.eliminarExperiencia, name='eliminarExperiencia'),
                url(r'^eliminar/eliminarexperienciaAux/(?P<id>[0-9]+)$', views.eliminarExperienciaAux, name='eliminarExperienciaAux'),

                

            ]
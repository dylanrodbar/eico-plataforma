from django.conf.urls import url, include
from . import views


app_name = "forum"

urlpatterns = [ 
                url(r'^escuela/$', views.viewEscuela, name='viewEscuela'),
                url(r'^escuela/nueva$', views.newEscuela, name='newEscuela'),
                
                url(r'^egresado/$', views.viewEgresado, name='viewEgresado'),  
                url(r'^egresado/nueva$', views.newEgresado, name='newEgresado'), 

                url(r'^insertarPost/$', views.insertarPost, name='insertarPost'),

                url(r'^changePost/(?P<id>[0-9]+)/$', views.changePost, name='changePost'),

                url(r'^editar/(?P<id>[0-9]+)/$', views.editNoticia, name="editNoticia"),

                url(r'^eliminar/(?P<id>[0-9]+)/$', views.deleteNoticia, name="deleteNoticia"),

                url(r'^eliminar/(?P<id>[0-9]+)/$', views.deleteNoticia, name="deleteNoticia"),

                url(r'^eliminar/eliminarpublicacionAux/(?P<id>[0-9]+)/$', views.eliminarPublicacionAux, name="eliminarPublicacionAux"),


                url(r'^noticia/calificarrelevante/(?P<id>[0-9]+)/$', views.calificarNoticiaRelevante, name="calificarNoticiaRelevante"),

                url(r'^noticia/calificarindiferente/(?P<id>[0-9]+)/$', views.calificarNoticiaIndiferente, name="calificarNoticiaIndiferente"),

                url(r'^noticia/calificaremocionante/(?P<id>[0-9]+)/$', views.calificarNoticiaEmocionante, name="calificarNoticiaEmocionante"),

                url(r'^ver/(?P<id>[0-9]+)/$', views.viewNoticia, name="viewNoticia"),

                url(r'^insertarComentario/(?P<id>[0-9]+)/$', views.insertarComentario, name="insertarComentario"),

                url(r'^escuela/anteriorescuela/$', views.anteriorEscuela, name="anteriorEscuela"),
                url(r'^escuela/siguienteescuela/$', views.siguienteEscuela, name="siguienteEscuela"),
                url(r'^egresados/anterioregresados/$', views.anteriorEgresados, name="anteriorEgresados"),
                url(r'^egresados/siguienteegresados/$', views.siguienteEgresados, name="siguienteEgresados"),

                url(r'^buscarUsuarioEscuela/$', views.buscarUsuarioEscuela, name="buscarUsuarioEscuela"),
                url(r'^buscarUsuarioEgresado/$', views.buscarUsuarioEgresado, name="buscarUsuarioEgresado"),
                url(r'^buscarNoticiaEscuela/$', views.buscarNoticiaEscuela, name="buscarNoticiaEscuela"),
                url(r'^buscarNoticiaEgresado/$', views.buscarNoticiaEgresado, name="buscarNoticiaEgresado"),
                
                
                
                              
            ]
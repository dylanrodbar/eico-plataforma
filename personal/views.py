from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection
#from django.urls import reverse
from django.core.urlresolvers import reverse

import cloudinary.uploader

cloudinary.config(
    cloud_name = 'poppycloud',
    api_key = '328358331617938',
    api_secret = 'z-7k70XpvP1dl1ZdiqVF0olXp7A'
)


# Create your views here.
def viewProfile(request):


    template = loader.get_template('personal/perfil.html')

    print("hola")
    print(request.session['Usuario'])

    id_usuario = request.session['Usuario']

    print(id_usuario)


    cur = connection.cursor()
    cur.callproc('obtener_usuario_id', [id_usuario,])
    datos_usuario = cur.fetchall()

    print(datos_usuario)

    cur.nextset()
    cur.callproc('obtener_publicaciones_usuario', [id_usuario, ])
    publicaciones_usuario = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_experiencias_o_proyectos_usuario', [id_usuario])
    experiencia = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_educacion_usuario', [id_usuario])
    educacion = cur.fetchall()
    
    
    cur.close

    datos_usuario_detalle = datos_usuario[0]

    print(datos_usuario_detalle)

    context = {
        'datos_usuario': datos_usuario_detalle,
        'publicaciones_usuario': publicaciones_usuario,
        'educacion': educacion,
        'experiencia': experiencia
    }

    return HttpResponse(template.render(context, request))



# Create your views here.
def viewProfileUser(request, id):

    template = None
    print("holaaaaaa")
    if int(id) == int(request.session['Usuario']):
        template = loader.get_template('personal/perfil.html')
    else:
        template = loader.get_template('personal/perfilajeno.html')

    
    cur = connection.cursor()
    cur.callproc('obtener_usuario_id', [id,])
    datos_usuario = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_publicaciones_usuario', [id, ])
    publicaciones_usuario = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_experiencias_o_proyectos_usuario', [id])
    experiencia = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_educacion_usuario', [id])
    educacion = cur.fetchall()
    
    
    cur.close

    datos_usuario_detalle = datos_usuario[0]

    context = {
        'datos_usuario': datos_usuario_detalle,
        'publicaciones_usuario': publicaciones_usuario,
        'educacion': educacion,
        'experiencia': experiencia
    }

    return HttpResponse(template.render(context, request))



def editarPerfil(request):

    template = loader.get_template('personal/perfil.html')

    id_usuario = request.session['Usuario']

    nombre = request.POST.get('nombre')
    titulo = request.POST.get('titulo')
    puesto_actual = request.POST.get('puesto_actual')
    lugar_trabajo = request.POST.get('lugar_trabajo')
    correo_electronico = request.POST.get('correo_electronico')
    archivo = request.FILES.get("archivo")
    password = request.POST.get("password")

    imagen_subida = cloudinary.uploader.upload(archivo)

    # obtiene la referencia que va a permitir mostrar la imagen en la aplicación
    imagen_subida_url = imagen_subida["secure_url"]

    cur = connection.cursor()
    cur.callproc('editar_usuario', [id_usuario, nombre, correo_electronico, titulo, puesto_actual, lugar_trabajo, imagen_subida_url, password])
    cur.close

    return HttpResponseRedirect(reverse('perfil:viewProfile'))



def agregarExperienciaOTrabajo(request):
    template = loader.get_template('personal/perfil.html')
    id_usuario = request.session['Usuario']

    id_usuario = request.session['Usuario']

    puesto = request.POST.get('puestoexperiencia')
    trabajo = request.POST.get('trabajoexperiencia')
    fecha_inicio = request.POST.get('finicioexperiencia')
    fecha_final = request.POST.get('ffinalexperiencia')
    descripcion = request.POST.get('descripcionexperiencia')

    cur = connection.cursor()
    cur.callproc('insertar_experiencia_o_proyecto', [puesto, trabajo, fecha_inicio, fecha_final, descripcion, id_usuario])
    cur.close
    
    return HttpResponseRedirect(reverse('perfil:viewProfile'))

def agregarEducacion(request):
    template = loader.get_template('personal/perfil.html')

    id_usuario = request.session['Usuario']

    titulo = request.POST.get('tituloeducacion')
    centro_educativo = request.POST.get('centroeducativoeducacion')
    fecha_inicio = request.POST.get('finicioeducacion')
    fecha_final = request.POST.get('ffinaleducacion')
    descripcion = request.POST.get('descripcioneducacion')

    print(titulo)

    cur = connection.cursor()
    cur.callproc('insertar_educacion', [titulo, centro_educativo, fecha_inicio, fecha_final, descripcion, id_usuario])
    cur.close
    
    return HttpResponseRedirect(reverse('perfil:viewProfile'))



def editarEducacion(request, id):
    template = loader.get_template('personal/editareducacion.html')
    context = {
        'id': id
    }
    return HttpResponse(template.render(context, request))


def editarEducacionAux(request, id):
    template = loader.get_template('personal/editareducacion.html')
    
    id_usuario = request.session['Usuario']
    titulo = request.POST.get('tituloeducacion')
    centro_educativo = request.POST.get('centroeducativoeducacion')
    fecha_inicio = request.POST.get('finicioeducacion')
    fecha_final = request.POST.get('ffinaleducacion')
    descripcion = request.POST.get('descripcioneducacion')

    

    cur = connection.cursor()
    cur.callproc('editar_educacion', [id, titulo, centro_educativo, fecha_inicio, fecha_final, descripcion, id_usuario])
    cur.close
    return HttpResponseRedirect(reverse('perfil:viewProfile'))



def editarExperiencia(request, id):
    template = loader.get_template('personal/editarexperiencia.html')
    context = {
        'id': id
    }
    return HttpResponse(template.render(context, request))


def editarExperienciaAux(request, id):
    template = loader.get_template('personal/editarexperiencia.html')
    
    id_usuario = request.session['Usuario']

    puesto = request.POST.get('puestoexperiencia')
    trabajo = request.POST.get('trabajoexperiencia')
    fecha_inicio = request.POST.get('finicioexperiencia')
    fecha_final = request.POST.get('ffinalexperiencia')
    descripcion = request.POST.get('descripcionexperiencia')


    cur = connection.cursor()
    cur.callproc('editar_experiencia_o_proyecto', [id, puesto, trabajo, fecha_inicio, fecha_final, descripcion, id_usuario])
    cur.close
    return HttpResponseRedirect(reverse('perfil:viewProfile'))


def eliminarEducacion(request, id):
    template = loader.get_template('personal/eliminareducacion.html')
    
    context = {
        'id': id
    }
    
    return HttpResponse(template.render(context, request))
    
def eliminarEducacionAux(request, id):
    template = loader.get_template('personal/eliminareducacion.html')
    context = {}
    print("hola")
    cur = connection.cursor()
    cur.callproc('eliminar_educacion', [id])
    cur.close

    return HttpResponseRedirect(reverse('perfil:viewProfile'))




def eliminarExperiencia(request, id):

    template = loader.get_template('personal/eliminarexperiencia.html')
    
    context = {
        'id': id
    }
    
    return HttpResponse(template.render(context, request))
    
    

def eliminarExperienciaAux(request, id):
    template = loader.get_template('personal/eliminarexperiencia.html')
    context = {}
    print("hola")
    cur = connection.cursor()
    cur.callproc('eliminar_experiencia', [id])
    cur.close

    return HttpResponseRedirect(reverse('perfil:viewProfile'))

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection
#from django.urls import reverse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail


import cloudinary.uploader
import math

cloudinary.config(
    cloud_name = 'poppycloud',
    api_key = '328358331617938',
    api_secret = 'z-7k70XpvP1dl1ZdiqVF0olXp7A'
)

def convertir_tupla_lista(tupla):
    lista = []
    largo = len(tupla)
    for i in range(largo):
        lista.append(list(tupla[i]))
    return lista


def convertir_lista_tupla(lista):
    largo = len(lista)
    for i in range(largo):
        lista[i] = tuple(lista[i])
    lista = tuple(lista)
    return lista
    

def viewEscuela(request):
    template = loader.get_template('forum/escuela.html')

    request.session['CuentaPublicaciones'] = 0
    numero_fila = request.session['CuentaPublicaciones']
    
    numero_fila = numero_fila * 4

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_escuela', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()

    cur.callproc('obtener_todas_publicaciones_escuela', [])
    publicaciones_todas = cur.fetchall()
    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_escuela', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

    largo_noticias_todas = len(publicaciones_todas)
    numero_grupos = math.ceil((largo_noticias_todas / 4))
    request.session['LimitePublicaciones'] = numero_grupos
    
    
    
    context = {
   	    'noticias': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))

    #return render(request, 'forum/escuela.html')

def viewEgresado(request):
    template = loader.get_template('forum/egresado.html')

    request.session['CuentaPublicaciones'] = 0
    numero_fila = request.session['CuentaPublicaciones']
    
    numero_fila = numero_fila * 4

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_egresados', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()

    cur.callproc('obtener_todas_publicaciones_egresados', [])
    publicaciones_todas = cur.fetchall()
    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_egresados', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

    largo_noticias_todas = len(publicaciones_todas)
    numero_grupos = math.ceil((largo_noticias_todas / 4))
    request.session['LimitePublicaciones'] = numero_grupos
    
    
    
    context = {
   	    'egresados': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))
    #return render(request, 'forum/egresado.html')

def newEgresado(request):
	return render(request, 'forum/nuevaNoticia.html')

def newEscuela(request):
	return render(request, 'forum/nuevaNoticia.html')

def insertarPost(request):

    template = loader.get_template('forum/nuevaNoticia.html')

    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    link_video = request.POST.get('video')
    file = request.FILES.get("archivo")

    embed_link_video = link_video.replace("watch?v=", "embed/")

    user = int(request.session['Usuario'])

    imagen_subida = cloudinary.uploader.upload(file)

    #obtiene la referencia que va a permitir mostrar la imagen en la aplicación
    imagen_subida_url = imagen_subida["secure_url"]

    cur = connection.cursor()
    cur.callproc('insertar_publicacion', [titulo, descripcion, embed_link_video, imagen_subida_url, user])
    cur.nextset()
    cur.callproc('obtener_correos_electronicos_sin_administradores', [])
    correos = cur.fetchall()
    cur.close
    
    lista_correos = []
    largo = len(correos)
    for i in range(largo):
        lista_correos.append(correos[i][0])

    seccion = "Escuela"
    if request.session['TipoUsuario'] == "Egresado":
        seccion = "Egresados"


    mensaje = "Notificación de una nueva noticia en la sección de: "+seccion+". Título: "+titulo
    
    send_mail('Notificación de nueva noticia',
             mensaje, 
             'eicocuenta@gmail.com',
             lista_correos)

    
    return HttpResponseRedirect(reverse('forum:viewEscuela'))


def viewNoticia(request, id):

    template = loader.get_template('forum/detalleNoticia.html')

    cur = connection.cursor()
    cur.callproc('obtener_publicacion_id', [id, ])
    publicacion = cur.fetchall()

    cur.nextset()


    cur.callproc('obtener_comentarios_publicacion', [id, ])
    comentarios = cur.fetchall()

    cur.nextset()

    cur.callproc('obtener_relevante_publicacion', [id, ])

    relevantes = cur.fetchall()

    cur.nextset()

    cur.callproc('obtener_indiferente_publicacion', [id, ])

    indiferentes = cur.fetchall()

    cur.nextset()

    cur.callproc('obtener_emocionante_publicacion', [id, ])

    emocionantes = cur.fetchall()

    cur.close()

    
    context = {
        'publicacion': publicacion[0],
        'comentarios': comentarios,
        'relevantes': relevantes[0],
        'indiferentes': indiferentes[0],
        'emocionantes': emocionantes[0],
        'id': id
    }

    return HttpResponse(template.render(context, request))



def editNoticia(request, id):
    template = loader.get_template('forum/editarNoticia.html')
    context = {
        "id": id,

    }
    return HttpResponse(template.render(context, request))


def changePost(request, id):
    template = loader.get_template('forum/editarNoticia.html')

    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    link_video = request.POST.get('video')
    file = request.FILES.get("archivo")

    embed_link_video = link_video.replace("watch?v=", "embed/")

    user = int(request.session['Usuario'])

    imagen_subida = cloudinary.uploader.upload(file)

    # obtiene la referencia que va a permitir mostrar la imagen en la aplicación
    imagen_subida_url = imagen_subida["secure_url"]

    cur = connection.cursor()
    cur.callproc('editar_publicacion', [id, titulo, descripcion, embed_link_video, imagen_subida_url])
    cur.close

    return HttpResponseRedirect(reverse('perfil:viewProfile'))




def deleteNoticia(request, id):
    template = loader.get_template('forum/eliminarpublicacion.html')
    
    context = {
        'id': id
    }
    
    return HttpResponse(template.render(context, request))
    
def eliminarPublicacionAux(request, id):
    template = loader.get_template('forum/eliminarpublicacion.html')

    cur = connection.cursor()
    cur.callproc('eliminar_publicacion', [id,])
    cur.close

    return HttpResponseRedirect(reverse('perfil:viewProfile'))


def insertarComentario(request, id):
    template = loader.get_template('forum/detalleNoticia.html')

    print("ENTRA A COMENTARIOS")
    id_usuario = int(request.session['Usuario'])
    id_publicacion = id
    comentario = request.POST.get('comentario')

    cur = connection.cursor()
    cur.callproc('insertar_comentario_publicacion', [comentario, id_usuario, id_publicacion])
    cur.close

    #return HttpResponseRedirect("") 
    #redirect_to = reverse('forum:viewNoticia', kwargs={'id': id})
    #return redirect(redirect_to)
    #return HttpResponseRedirect(viewNoticia, id)
    return HttpResponseRedirect(reverse('forum:viewNoticia', args=[id]))

def calificarNoticiaRelevante(request, id):
    template = loader.get_template('forum/detalleNoticia.html')

    id_usuario = int(request.session['Usuario'])
    id_publicacion = id
    calificacion = "Relevante"

    cur = connection.cursor()
    cur.callproc('obtener_id_calificacion', [calificacion,])
    id_calificacion_tupla = cur.fetchall()
    

    id_calificacion = id_calificacion_tupla[0][0]

    
    cur.nextset()
    cur.callproc('calificar_publicacion', [id_publicacion,id_calificacion,id_usuario])

    cur.close

    return HttpResponseRedirect(reverse('forum:viewNoticia', args=[id])) 


def calificarNoticiaIndiferente(request, id):
    template = loader.get_template('forum/detalleNoticia.html')

    id_usuario = int(request.session['Usuario'])
    id_publicacion = id
    calificacion = "Indiferente"

    cur = connection.cursor()
    cur.callproc('obtener_id_calificacion', [calificacion,])
    id_calificacion_tupla = cur.fetchall()
    

    id_calificacion = id_calificacion_tupla[0][0]

    
    cur.nextset()
    cur.callproc('calificar_publicacion', [id_publicacion,id_calificacion,id_usuario])

    cur.close

    return HttpResponseRedirect(reverse('forum:viewNoticia', args=[id])) 


def calificarNoticiaEmocionante(request, id):
    template = loader.get_template('forum/detalleNoticia.html')

    id_usuario = int(request.session['Usuario'])
    id_publicacion = id
    calificacion = "Emocionante"

    cur = connection.cursor()
    cur.callproc('obtener_id_calificacion', [calificacion,])
    id_calificacion_tupla = cur.fetchall()
    

    id_calificacion = id_calificacion_tupla[0][0]

    
    cur.nextset()
    cur.callproc('calificar_publicacion', [id_publicacion,id_calificacion,id_usuario])

    cur.close

    return HttpResponseRedirect(reverse('forum:viewNoticia', args=[id])) 
    

def anteriorEscuela(request):
    template = loader.get_template('forum/escuela.html')

    numero_fila = request.session['CuentaPublicaciones']
    numero_grupos = request.session['LimitePublicaciones']
    
    numero_fila -= 1
    if numero_fila < 0:
        numero_fila = 0

    numero_fila = numero_fila * 4

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_escuela', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_escuela', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

        
    #numero_grupos = math.ceil((largo_noticias / 4))
    #request.session['LimiteNoticias'] = numero_grupos
    #print(request.session['LimiteNoticias'])

    
    
    context = {
   	    'noticias': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))

    #return render(request, 'forum/escuela.html')


def siguienteEscuela(request):
    template = loader.get_template('forum/escuela.html')

    numero_fila = request.session['CuentaPublicaciones']
    numero_grupos = request.session['LimitePublicaciones']
    print(numero_grupos)
    numero_fila += 1
    if numero_fila > numero_grupos:
        numero_fila = numero_grupos
    
    numero_fila = numero_fila * 4

    
    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_escuela', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_escuela', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

        
    #numero_grupos = math.ceil((largo_noticias / 4))
    #request.session['LimiteNoticias'] = numero_grupos
    #print(request.session['LimiteNoticias'])

    
    
    context = {
   	    'noticias': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))

    #return render(request, 'forum/escuela.html')




def anteriorEgresados(request):
    template = loader.get_template('forum/egresado.html')

    numero_fila = request.session['CuentaPublicaciones']
    numero_grupos = request.session['LimitePublicaciones']
    
    numero_fila -= 1
    if numero_fila < 0:
        numero_fila = 0

    numero_fila = numero_fila * 4

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_egresados', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_egresados', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

        
    #numero_grupos = math.ceil((largo_noticias / 4))
    #request.session['LimiteNoticias'] = numero_grupos
    #print(request.session['LimiteNoticias'])

    
    
    context = {
   	    'egresados': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))

    #return render(request, 'forum/escuela.html')


def siguienteEgresados(request):
    template = loader.get_template('forum/egresado.html')

    numero_fila = request.session['CuentaPublicaciones']
    numero_grupos = request.session['LimitePublicaciones']
    print(numero_grupos)
    numero_fila += 1
    if numero_fila > numero_grupos:
        numero_fila = numero_grupos
    numero_fila = numero_fila * 4

    
    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_egresados', [numero_fila])
    noticias = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_top_publicaciones_relevantes_egresados', [])
    
    noticias_relevantes = cur.fetchall()

    
    lista = convertir_tupla_lista(noticias)

    largo_noticias = len(lista)

    
    for i in range(largo_noticias):
        indice = lista[i]
        id_c = indice[0]
        cur.nextset()
        cur.callproc('obtener_relevante_publicacion', [id_c])
        cantidad_relevantes = cur.fetchall()
        elemento = cantidad_relevantes[0][0]
        lista[i].append(elemento)

    noticias = convertir_lista_tupla(lista)

    cur.nextset()
    cur.close

        
    #numero_grupos = math.ceil((largo_noticias / 4))
    #request.session['LimiteNoticias'] = numero_grupos
    #print(request.session['LimiteNoticias'])

    
    
    context = {
   	    'egresados': noticias,
        'noticiasrelevantes': noticias_relevantes
    }
    return HttpResponse(template.render(context, request))

    #return render(request, 'forum/escuela.html')


def buscarUsuarioEscuela(request):
    template = loader.get_template('forum/usuariosbuscados.html')

    nombreusuario = request.POST.get('nombreusuario')
    
    formatoinicio = '%'
    formatofinal = '%'

    parametro = formatoinicio + nombreusuario + formatofinal
    print(parametro)

    cur = connection.cursor()
    cur.callproc('obtener_usuarios_substring_no_egresados', [parametro])
    usuarios = cur.fetchall()

    

    context = {
   	    'usuarios': usuarios,
    }
    return HttpResponse(template.render(context, request))


def buscarUsuarioEgresado(request):
    template = loader.get_template('forum/usuariosbuscados.html')

    nombreusuario = request.POST.get('nombreusuario')
    
    formatoinicio = '%'
    formatofinal = '%'

    parametro = formatoinicio + nombreusuario + formatofinal
    print(parametro)

    cur = connection.cursor()
    cur.callproc('obtener_usuarios_substring_egresados', [parametro])
    usuarios = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_experiencias_o_proyectos_substring', [parametro])
    experiencias = cur.fetchall()

    print(experiencias)
    
    

    context = {
   	    'usuarios': usuarios,
        'experiencias': experiencias
    }
    return HttpResponse(template.render(context, request))


def buscarNoticiaEscuela(request):
    template = loader.get_template('forum/noticiasbuscadas.html')

    nombrenoticia = request.POST.get('nombrenoticia')



    formatoinicio = '%'
    formatofinal = '%'

    parametro = formatoinicio + nombrenoticia + formatofinal
    print(parametro)

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_substring_no_egresados', [parametro])
    noticias = cur.fetchall()

    

    context = {
   	    'noticias': noticias,
    }
    return HttpResponse(template.render(context, request))


def buscarNoticiaEgresado(request):
    template = loader.get_template('forum/noticiasbuscadas.html')

    nombrenoticia = request.POST.get('nombrenoticia')
    
    formatoinicio = '%'
    formatofinal = '%'

    parametro = formatoinicio + nombrenoticia + formatofinal
    print(parametro)

    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_substring_egresados', [parametro])
    noticias = cur.fetchall()

    

    context = {
   	    'noticias': noticias,
    }
    return HttpResponse(template.render(context, request))
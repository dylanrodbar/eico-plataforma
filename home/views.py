from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection
#from django.urls import reverse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

import os
import numpy as np
import Excel
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import threading

import cloudinary.uploader

cloudinary.config(
    cloud_name = 'poppycloud',
    api_key = '328358331617938',
    api_secret = 'z-7k70XpvP1dl1ZdiqVF0olXp7A'
)


def esTodoCero(datos):
    for i in datos:
        if i != 0:
            return False
    return True

def generarGrafico(nombre, datosGrafico):
    #plt.switch.backend y plt.close se usan para no generar errores de hilos en matplotlib
    plt.switch_backend('Agg')
    if not esTodoCero(datosGrafico):
        fig = plt.figure(u"Reacciones") # Figure
        ax = fig.add_subplot(111) # Axes
        nombres = ['Relevante', 'Indiferente', 'Emocionante']
        datos = [datosGrafico[0], datosGrafico[1], datosGrafico[2]]

            

        xx = range(len(datos))

        ax.bar(xx, datos, width=0.8, align='center')
        ax.set_xticks(xx)
        ax.set_xticklabels(nombres)

        plt.title("Reacciones para: "+nombre)

        plt.savefig("Grafico"+nombre+".png")
        imagen_subida = cloudinary.uploader.upload("Grafico"+nombre+".png")

        #obtiene la referencia que va a permitir mostrar la imagen en la aplicación
        imagen_subida_url = imagen_subida["secure_url"]

        plt.close()        

        return imagen_subida_url
    else:
        return None
    

def generarGraficoVisitas(nombre, datosGrafico):
    

    #plt.switch.backend y plt.close se usan para no generar errores de hilos en matplotlib
    plt.switch_backend('Agg')
    if not esTodoCero(datosGrafico):
        fig = plt.figure(u"Visitas") # Figure
        ax = fig.add_subplot(111) # Axes
        nombres = ['Visitas']
        datos = [datosGrafico[0]]

            

        xx = range(len(datos))

        ax.bar(xx, datos, width=0.4, align="edge")
        ax.set_xticks(xx)
        ax.set_xticklabels(nombres)

        plt.title("Visitas para: "+nombre)

        plt.savefig("Grafico"+nombre+".png")
        imagen_subida = cloudinary.uploader.upload("Grafico"+nombre+".png")

        #obtiene la referencia que va a permitir mostrar la imagen en la aplicación
        imagen_subida_url = imagen_subida["secure_url"]

        plt.close()


        return imagen_subida_url
    else:
        return None

def generarGraficos(lista_graficos, lista_graficos_fechas):

    contador = 0
    lista_direcciones = []
    print(lista_graficos)
    for i in lista_graficos_fechas:
        

        fecha = str(i.day)+"-"+str(i.month)+"-"+str(i.year)
        elemento = generarGrafico(fecha, lista_graficos[contador])
        if elemento != None:
            lista_direcciones.append(generarGrafico(fecha, lista_graficos[contador]))
        
        #plt.show()
        
        contador += 1

        #imagen_subida = cloudinary.uploader.upload(img)

        #obtiene la referencia que va a permitir mostrar la imagen en la aplicación
        #imagen_subida_url = imagen_subida["secure_url"]
    return lista_direcciones
    

def generarGraficosVisitas(lista_graficos, lista_graficos_fechas):

    contador = 0
    lista_direcciones = []
    print(lista_graficos)
    for i in lista_graficos_fechas:
        

        fecha = str(i.day)+"-"+str(i.month)+"-"+str(i.year)
        elemento = generarGraficoVisitas(fecha, lista_graficos[contador])
        if elemento != None:

            lista_direcciones.append(generarGraficoVisitas(fecha, lista_graficos[contador]))
        
        #plt.show()
        
        contador += 1

        #imagen_subida = cloudinary.uploader.upload(img)

        #obtiene la referencia que va a permitir mostrar la imagen en la aplicación
        #imagen_subida_url = imagen_subida["secure_url"]
    return lista_direcciones
    



def obtenerValoresGraficosVisitas(lista_graficos, visitas):
    largo_visitas = len(visitas)
    for i in range(largo_visitas):
        lista_graficos[i][0] = visitas[i][0]
    return lista_graficos
    
    
def obtenerValoresGraficos(lista_graficos, relevantes, indiferentes, emocionantes):
    largo_relevantes = len(relevantes)
    largo_indiferentes = len(indiferentes)
    largo_emocionantes = len(emocionantes)

    for i in range(largo_relevantes):
        lista_graficos[i][0] = relevantes[i][0]
    for i in range(largo_indiferentes):
        lista_graficos[i][1] = indiferentes[i][0]
    for i in range(largo_emocionantes):
        lista_graficos[i][2] = emocionantes[i][0]
    return lista_graficos


def obtenerFechas():
    lista = []
    lista.append(datetime.datetime.now())
    contador = 1
    while contador <= 6:
        lista.append(datetime.datetime.now() - datetime.timedelta(days=contador))
        contador += 1
    return lista

def obtenerValoresGraficosFechasVisitas(lista_graficos, visitas):
    largo_visitas = len(visitas)
    
    for i in range(largo_visitas):
        lista_graficos[i][0] = visitas[i][1]
    return lista_graficos

def obtenerValoresGraficosFechas(lista_graficos, relevantes, indiferentes, emocionantes):
    largo_relevantes = len(relevantes)
    largo_indiferentes = len(indiferentes)
    largo_emocionantes = len(emocionantes)

    for i in range(largo_relevantes):
        lista_graficos[i][0] = relevantes[i][1]
    for i in range(largo_indiferentes):
        lista_graficos[i][1] = indiferentes[i][1]
    for i in range(largo_emocionantes):
        lista_graficos[i][2] = emocionantes[i][1]
    return lista_graficos
    

def inicializarGraficosVisitas():
    return [[0],[0],[0],[0],[0],[0],[0]]
def inicializarGraficosReacciones():
    return [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

def enviarCorreosElectronicos():
    send_mail('Prueba de envío de correos varios usuarios', 'Im Poppy', 'pdjango123@gmail.com', ['dylanrodbar97@gmail.com', 'josemorar96@gmail.com ', 'karizp14@gmail.com '])
    

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

def dividirListaGruposTres(lista):
    lista_retorno = []
    elemento_lista = []
    largo = len(lista)
    if largo <= 3:
        lista_retorno.append(lista)
        lista_retorno.append([])
    else:
        elemento_lista = lista[:3]
        lista_retorno.append(elemento_lista)
        lista_retorno.append(lista[3:])
    return lista_retorno


def dividirListaGruposCuatro(lista):
    lista_retorno = []
    elemento_lista = []
    largo = len(lista)
    if largo <= 4:
        lista_retorno.append(lista)
        lista_retorno.append([])
    else:
        while(largo > 4):
            elemento_lista = lista[:4]
            lista_retorno.append(elemento_lista)
            lista = lista[4:]
            largo = len(lista)
        lista_retorno.append(lista)
    return lista_retorno

def estadisticasVisitasAux(request):
    template = loader.get_template('home/admin.html')

    cur = connection.cursor()
    cur.callproc('obtener_sitios_interes', [])
    sitios = cur.fetchall()


    cur.nextset()

    cur.callproc('obtener_servicios', [])
    servicios = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_calendario', [])
    calendarios = cur.fetchall()
    cur.nextset()
    cur.callproc('obtener_visitas', [])
    visitas = cur.fetchall()
    
    cur.close

    inicio_valores = inicializarGraficosVisitas()
    valores_graficos = obtenerValoresGraficosVisitas(inicio_valores, visitas)
    valores_graficos_fechas = obtenerFechas()

    direcciones = generarGraficosVisitas(valores_graficos, valores_graficos_fechas)

    plt.close('all')
    
    context = {
        'sitiosinteres': sitios,
        'servicios': servicios,
        'calendarios': calendarios,
        'id': 0,
        'direcciones': direcciones
    }
    return HttpResponse(template.render(context, request))


def estadisticasVisitas(request):
    template = loader.get_template('home/admin.html')
    return HttpResponseRedirect(reverse('home:estadisticasVisitasAux'))

def estadisticasReaccionesAux(request):
    template = loader.get_template('home/admin.html')

    cur = connection.cursor()
    cur.callproc('obtener_sitios_interes', [])
    sitios = cur.fetchall()


    cur.nextset()

    cur.callproc('obtener_servicios', [])
    servicios = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_calendario', [])
    calendarios = cur.fetchall()
    cur.nextset()
    cur.callproc('obtener_relevantes', [])
    relevantes = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_indiferentes', [])
    indiferentes = cur.fetchall()
    
    cur.nextset()
    cur.callproc('obtener_emocionantes', [])
    emocionantes = cur.fetchall()
    
    cur.close

    inicio_valores = inicializarGraficosReacciones()
    valores_graficos = obtenerValoresGraficos(inicio_valores, relevantes, indiferentes, emocionantes)
    valores_graficos_fechas = obtenerFechas()

    
    direcciones = generarGraficos(valores_graficos, valores_graficos_fechas)
    
    plt.close('all')

    context = {
        'sitiosinteres': sitios,
        'servicios': servicios,
        'calendarios': calendarios,
        'id': 0,
        'direcciones': direcciones
    }
    return HttpResponse(template.render(context, request))


def estadisticasReacciones(request):
    template = loader.get_template('home/admin.html')
    return HttpResponseRedirect(reverse('home:estadisticasReaccionesAux'))

    

def index(request):
    template = loader.get_template('home/index.html')

    request.session['Mes'] = 0
    request.session['Anio'] = 0
    request.session['CuentaPublicaciones'] = 0
    request.session['LimitePublicaciones'] = 0
        
    
    cur = connection.cursor()
    cur.callproc('obtener_publicaciones_recientes', ())
    publicaciones = cur.fetchall()
    cur.nextset()

    cur.callproc('insertar_visita', [])
    cur.nextset()

    cur.close()

    lista_publicaciones = convertir_tupla_lista(publicaciones)
    
    lista_acomodada = dividirListaGruposTres(lista_publicaciones)
    lista_acomodada_tupla = convertir_lista_tupla(lista_acomodada)

    print(lista_acomodada_tupla)
    context = {
        'noticias': lista_acomodada_tupla
    }

    return HttpResponse(template.render(context, request))

    #return render(request, 'home/index.html')


def errorLogin(request):
    template = loader.get_template('home/index.html')
    context = {
        'error': "El usuario o contraseña es incorrecto"
    }

    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('home/header.html')
    context = {}
    username = request.POST.get('email')
    password = str(request.POST.get('password'))
    cur = connection.cursor()
    login = cur.callproc('iniciar_sesion', [username, password])
    login = cur.fetchall()
    cur.close
    if login == ():
        return HttpResponseRedirect(reverse('home:errorLogin'))
    else:
        request.session['Usuario'] = login[0][0]
        request.session['IdTipoUsuario'] = login[0][1]
        request.session['TipoUsuario'] = login[0][2]
        
        return HttpResponseRedirect(reverse('forum:viewEscuela'))
        # if login[0][1] == "Administrador":
        #    return HttpResponseRedirect(reverse('blog:noticias'))
        # elif login[0][1] == "Cliente":
        #    return HttpResponseRedirect(reverse('blogClient:noticias'))


def logout(request):
    template = loader.get_template('home/header.html')

    del request.session['Usuario']
    del request.session['TipoUsuario']
    del request.session['IdTipoUsuario']

    request.session.modified = True

    return HttpResponseRedirect(reverse('forum:viewEscuela'))


def viewService(request):
    template = loader.get_template('home/servicio.html')

    cur = connection.cursor()
    cur.callproc('obtener_servicios', [])
    servicios = cur.fetchall()
    cur.close

    lista_publicaciones = convertir_tupla_lista(servicios)
    
    lista_acomodada = dividirListaGruposCuatro(lista_publicaciones)
    lista_acomodada_tupla = convertir_lista_tupla(lista_acomodada)
    

    context = {
        'servicios': lista_acomodada_tupla
    }
    return HttpResponse(template.render(context, request))


def viewInteres(request):
    template = loader.get_template('home/interes.html')

    cur = connection.cursor()
    cur.callproc('obtener_sitios_interes', [])
    sitios = cur.fetchall()
    cur.close



    lista_publicaciones = convertir_tupla_lista(sitios)
    
    lista_acomodada = dividirListaGruposCuatro(lista_publicaciones)
    lista_acomodada_tupla = convertir_lista_tupla(lista_acomodada)
    
    context = {
        'sitiosinteres': lista_acomodada_tupla
    }
    return HttpResponse(template.render(context, request))


def admin(request):
    template = loader.get_template('home/admin.html')

    cur = connection.cursor()
    cur.callproc('obtener_sitios_interes', [])
    sitios = cur.fetchall()


    cur.nextset()

    cur.callproc('obtener_servicios', [])
    servicios = cur.fetchall()

    cur.nextset()
    cur.callproc('obtener_calendario', [])
    calendarios = cur.fetchall()
    cur.nextset()
    
    
    cur.close

    
    context = {
        'sitiosinteres': sitios,
        'servicios': servicios,
        'calendarios': calendarios,
        'id': 0,
        'direcciones': []
    }
    return HttpResponse(template.render(context, request))


def agregarUsuarios(request):
    template = loader.get_template('home/admin.html')

    file = request.FILES.get("archivo")

    elementos_excel = Excel.manejar_excel(file)

    print(elementos_excel)

    cur = connection.cursor()
    for i in (elementos_excel):
        usuario = i[0]
        contrasena = i[3]
        correo = i[1]
        media = 1
        tipo_usuario = str(i[2])
        cur.callproc('obtener_id_tipo_usuario', [tipo_usuario])
        tipo_usuario_nu = cur.fetchall()
        tipo_usuario_numero = tipo_usuario_nu[0][0]

        #se pregunta si el usuario ya existe
        cur.nextset()
        cur.callproc('obtener_usuario_existente', [correo])
        us = cur.fetchall()
        
        if us != ():
            cur.nextset()
            cur.callproc('editar_usuario_existente', [correo, usuario, tipo_usuario_numero])
            cur.nextset()

        else:
            cur.nextset()
            cur.callproc('insertar_usuario', [usuario, contrasena, correo, media, tipo_usuario_numero])
            cur.nextset()

    cur.close

    

    for i in (elementos_excel):
        correo = i[1]
        mensaje = "Se le notifica que su cuenta de usuario para nuestro sistema fue creada con éxito. Correo: "+i[1]+". Contraseña: "+i[3]
        send_mail('Notificación de creación de la cuenta solicitada',
             mensaje, 
             'eicocuenta@gmail.com',
             [correo])


    return HttpResponseRedirect(reverse('home:admin'))


def agregarSitio(request):
    template = loader.get_template('home/admin.html')
    titulo = request.POST.get('titulo-sitio')
    descripcion = request.POST.get('descripcion-sitio')
    cur = connection.cursor()
    cur.callproc('insertar_sitio_interes', [titulo, descripcion])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def agregarServicio(request):
    template = loader.get_template('home/admin.html')
    titulo = request.POST.get('titulo-servicio')
    descripcion = request.POST.get('descripcion-servicio')
    cur = connection.cursor()
    cur.callproc('insertar_servicio', [titulo, descripcion])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def editarSitio(request, id):
    template = loader.get_template('home/editarsitio.html')
    context = {
        'id': id
    }
    return HttpResponse(template.render(context, request))


def editarSitioAux(request, id):
    template = loader.get_template('home/editarsitio.html')
    titulo = request.POST.get('titulo')
    contenido = request.POST.get('descripcion')
    cur = connection.cursor()
    cur.callproc('editar_sitio_interes', [id, titulo, contenido])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def eliminarSitio(request, id):
    template = loader.get_template('home/eliminarsitio.html')
    context = {
        'id': id
    }
    
    return HttpResponse(template.render(context, request))

def eliminarSitioAux(request, id):
    template = loader.get_template('home/eliminarsitio.html')

    cur = connection.cursor()
    cur.callproc('eliminar_sitio_interes', [id])
    cur.close


    return HttpResponseRedirect(reverse('home:admin'))


def editarServicio(request, id):
    template = loader.get_template('home/editarservicio.html')
    context = {
        'id': id
    }
    return HttpResponse(template.render(context, request))


def editarServicioAux(request, id):
    template = loader.get_template('home/editarservicio.html')
    titulo = request.POST.get('titulo')
    contenido = request.POST.get('descripcion')
    cur = connection.cursor()
    cur.callproc('editar_servicio', [id, titulo, contenido])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def eliminarServicio(request, id):
    template = loader.get_template('home/eliminarservicio.html')
    
    context = {
        'id': id
    }

    return HttpResponse(template.render(context, request))


def eliminarServicioAux(request, id):
    template = loader.get_template('home/eliminarservicio.html')
    
    cur = connection.cursor()
    cur.callproc('eliminar_servicio', [id])
    cur.close

    return HttpResponseRedirect(reverse('home:admin'))


def agregarEvento(request):
    template = loader.get_template('home/admin.html')
    fecha = request.POST.get('fecha-evento')
    nombre = request.POST.get('nombre-evento')
    descripcion = request.POST.get('descripcion-evento')


    cur = connection.cursor()
    cur.callproc('insertar_calendario', [nombre, descripcion, fecha])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def editarEvento(request, id):
    template = loader.get_template('home/editarcalendario.html')
    context = {
        'id': id
    }
    return HttpResponse(template.render(context, request))

def editarEventoAux(request, id):
    template = loader.get_template('home/editarsitio.html')

    fecha = request.POST.get('fecha-evento')
    nombre = request.POST.get('nombre-evento')
    descripcion = request.POST.get('descripcion-evento')


    cur = connection.cursor()
    cur.callproc('editar_calendario', [id, nombre, descripcion, fecha])
    cur.close
    return HttpResponseRedirect(reverse('home:admin'))


def eliminarEvento(request, id):
    template = loader.get_template('home/eliminarcalendario.html')
    
    context = {
        'id': id
    }

    return HttpResponse(template.render(context, request))


def eliminarEventoAux(request, id):
    template = loader.get_template('home/eliminarcalendario.html')
    
    context = {}
    cur = connection.cursor()
    cur.callproc('eliminar_calendario', [id])
    cur.close

    return HttpResponseRedirect(reverse('home:admin'))


def solicitarUsuario(request):
    template = loader.get_template('home/header.html')
    
    nombresolicitud = request.POST.get('nombresolicitud')
    emailsolicitud = request.POST.get('emailsolicitud')
    descripcionsolicitud = request.POST.get('descripcionsolicitud')


    cur = connection.cursor()
    cur.callproc('obtener_correos_electronicos_administradores', [])
    correos = cur.fetchall()
    cur.close

    largo = len(correos)
    lista_emails = []
    for i in range(largo):
        lista_emails.append(correos[i][0])
    lista_emails.append("dylanrodbar97@gmail.com")

    mensaje = "Se requiere una cuenta para la de nombre: "+nombresolicitud+". Correo electrónico: "+emailsolicitud +". Debido a la siguiente razón: "+descripcionsolicitud

    send_mail('Solicitud de cuenta para el portal de EICO',
             mensaje, 
             'eicocuenta@gmail.com',
             lista_emails)


    send_mail('Solicitud de cuenta para el portal de EICO',
             'Estimado(a), se le comunica que se estará procesando su solicitud de la cuenta para nuestro portal, se le estará dando una pronta notificación', 
             'eicocuenta@gmail.com',
             [emailsolicitud])
    

    return HttpResponseRedirect(reverse('home:index'))

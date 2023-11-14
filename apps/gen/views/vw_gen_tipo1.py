from django.db import connection
from django.http import HttpResponse
from django.template import loader
import random
# @login_required(login_url="/login/")
# from core.encryption_util import EncryptDES
from utils.utils import dictfetchall
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from apps.gen.models import *
from django.core.exceptions import ObjectDoesNotExist
import json
from urllib.parse import unquote
def tipo1(request,tip_id,jue_id):
    # Lógica para obtener los datos del modelo Gen_Respuesta usando el jue_id
    respuestas = Gen_Respuesta.objects.filter(jue=jue_id)

    # Lógica para obtener los datos del modelo Gen_Juego usando el jue_id
    juego = Gen_Juego.objects.get(jue_id=jue_id)
    tipo_obj = Gen_Tipo.objects.get(tip_id=tip_id)
    tipo_codigo = int(tipo_obj.tip_codigo) if tipo_obj.tip_codigo.isdigit() else None
    multimedia=Gen_Multimedia.objects.filter(jue=jue_id)

    # Seleccionar el template correspondiente según el tip_id
    if tipo_codigo == 1:
        template_name = 'Juegos/Tipo1.html'
    elif tipo_codigo == 2:
        template_name = 'Juegos/Tipo2.html'
    elif tipo_codigo == 3:
        template_name = 'Juegos/Tipo3.html'
    elif tipo_codigo == 4:
        template_name = 'Juegos/Tipo4.html'
    else:
        # Si el tip_id no tiene un template correspondiente, devuelve un error o realiza otra acción según tus necesidades.
        return JsonResponse({'error': f'No hay un template disponible para el tip_id {tipo_codigo}'})

    # Preparar los datos que se enviarán al template como contexto en formato JSON
    data = {
        'juego': juego.__dict__,  # Convierte el modelo Gen_Juego a un diccionario
        'multimedia': list(multimedia.values()),
        'jue_id': jue_id,
        'tip_id': tip_id,
        'respuestas': list(respuestas.values()),  # Convertir el queryset a una lista de diccionarios
    }

    # Cargar el template usando loader.get_template
    html_template = loader.get_template(template_name)

    # Renderizar el template con los datos como contexto
    rendered_html = html_template.render(data)

    # Devolver el HTML renderizado como respuesta
    return HttpResponse(rendered_html)



def jugar_todos(request, json_data):
    json_str = unquote(json_data)
    juegos = json.loads(json_str)
    context = {
        'segment': 'tipos',
        'Juegos': juegos,
    }
    html_template = loader.get_template('Juegos/Tipos.html')
    return HttpResponse(html_template.render(context, request))
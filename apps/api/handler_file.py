# Autor: Dre
# Fecha: 17/12/2022 010:00
# Descripción: Vista para la opción categorias.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar
import json
import os

import django.db.models.query_utils
import pandas as pd
from django.db import transaction, connection
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.middleware import csrf
from django.shortcuts import redirect
#
_e = EncryptDES()

import json
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDict
from datetime import datetime


# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file_name = request.POST.get('myfile', '')
#         file_data = request.POST.get('myfile', '')
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#         print('INTERESANTE: ',file_path)
#         with open(file_path, 'wb+') as f:
#             f.write(file_data.encode())
#         return JsonResponse({'status': 'success'})
@csrf_exempt
def upload_file(request):

    for key in request.FILES.keys():

        # Itera sobre todas las claves en el MultiValueDict, o sea sobre
        # request.FILES
        values = request.FILES.getlist(key)

        if not values:
            return JsonResponse({'success': False, 'error': 'No se ha enviado ningún archivo'})

        myfile = values[0]
        extension_archivo = os.path.splitext(myfile.name)[1]  # obteniendo la extensión
        fs = FileSystemStorage()
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + extension_archivo
        fecha_hora_actual = fecha_hora_actual.replace(':', '-')  # Reemplazar los dos puntos con guiones
        fecha_hora_actual = fecha_hora_actual.replace(' ', '_')  # Reemplazar los espacios en blanco con guiones bajos
        # print(fecha_hora_actual)
        filename = fs.save(fecha_hora_actual, myfile)
        # Utiliza os.path.splitext para obtener la extensión del archivo
        extension = os.path.splitext(filename)[1]

        # Imprime la extensión del archivo
        # print('La extensión del archivo es:', extension)
        uploaded_file_url = fs.url(filename)
        # print(myfile, fs, filename, uploaded_file_url)
        # print('soydiospelado ', filename)
        return JsonResponse({'success': True, 'url': uploaded_file_url})
    else:
        # print('algoandamal')
        return JsonResponse({'success': False, 'error': 'No se ha enviado ningún archivo'})


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        file_url = request.POST.get('file_url')
        # print('vivalavidapelaoestoyeliminando ', file_url)
        # Verifica que la URL del archivo sea válida
        if file_url:
            # print('entresantamaria')
            # Elimina el archivo del sistema de archivos
            print(os.path)
            mediaurl = '/media/' + file_url
            fs = FileSystemStorage()
            # print('AMENODORIME', mediaurl)
            file_path = os.path.join(settings.MEDIA_ROOT, file_url)
            # print(file_path)
            fs.delete(file_path)
            mult = Gen_Multimedia.objects.filter(mul_archivo=mediaurl)
            # print('jeje')
            if mult.exists():
                # print('EEE ', mult[0].mul_id)
                mult[0].mul_estado = 0
                mult[0].save()
            return JsonResponse({'success': True, 'error': 'Eliminado'})
        else:
            return JsonResponse({'success': False, 'error': 'No eliminado'})


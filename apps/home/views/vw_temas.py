# # Autor: Bryan Amaya
#
# import random
# from django import template
# from django.contrib.auth.decorators import login_required
# from django.db import connection
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse
#
#
# # @login_required(login_url="/login/")
# from utils.utils import dictfetchall
#
#
# def temas(request):
#
#     with connection.cursor() as cursor:
#         # Se genera el cursos con el SQL para realizar la consulta
#         # cursor.execute(
#         #     """select * from gen.tema t where t.tem_estado = %s order by t.tem_id""",
#         #     ('1'))
#
#         cursor.execute(
#             """select * from gen.categoria c where c.cat_estado = %s order by c.cat_id""",
#             ('1'))
#
#         # el resultado de la consulta se lo transforma a lista de diccionarios
#         data = dictfetchall(cursor)
#
#
#         data_list = []
#         # Se tranfosrma de lista de diccionarios a JSON
#         for row in data:
#             l_row_dict = row
#             data_list.append(l_row_dict)
#             # Se trabaja con el data_list
#
#     rand_num = random.randrange(100000, 9999999)
#
#     # context2 = {'random': rand_num}
#     context = {'segment': 'temas',
#                'tema': data_list,
#                'random': rand_num}
#     html_template = loader.get_template('home/temas.html')
#     return HttpResponse(html_template.render(context, request))

# Autor: Bryan Amaya
import self
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
# _e = EncryptDES()
from django.db.models import Count
import json
from apps.sis.models import *
def temas(request,asi_id=None):
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()


    with connection.cursor() as cursor:
        # Se genera el cursos con el SQL para realizar la consulta
        # cursor.execute(
        #     """select * from gen.actividad a
        #        where a.tem_id = %s and a.act_estado  = %s""",
        #     (int(request.GET['tem']), '1'))

        # Si asi_id está presente, se agrega la condición a la consulta
        asi_condition = "AND t.asi_id = %s" if asi_id else ""
        cursor.execute(
            """SELECT 
                t.*, 
                a.asi_nombre, 
                COUNT(ta.tem_id) as numero_de_actividades,
                COALESCE(gm.mul_archivo, '/../static/img/Img-Template/classes-1.jpg') AS tema_imagen_url
                FROM gen.tema t
                JOIN gen.asignatura a ON t.asi_id = a.asi_id
                LEFT JOIN gen.tema_actividad ta ON t.tem_id = ta.tem_id
                LEFT JOIN gen.multimedia gm ON t.tem_id = gm.tem_id AND gm.act_id IS NULL AND gm.jue_id IS NULL AND gm.res_id IS NULL
                WHERE t.tem_estado = 1 {} 
                GROUP BY t.tem_id, a.asi_nombre, gm.mul_archivo
                ORDER BY t.tem_id;
            """.format(asi_condition),
            (asi_id,) if asi_id else ()
        )

        # el resultado de la consulta se lo transforma a lista de diccionarios
        data = dictfetchall(cursor)
        data_list = []
        cursor.execute(
            """select * from gen.asignatura a 
               where  a.asi_estado  = %s""",
            ('1'))
        data2 = dictfetchall(cursor)
        data_list2 = []

        cursor.execute(
            """select * from gen.multimedia m 
               where  m.mul_estado  = %s
               order by m.mul_id""",
            ('1'))
        data3 = dictfetchall(cursor)
        data_list3 = []

        # Se tranfosrma de lista de diccionarios a JSON
        for row in data:
            l_row_dict = row
            data_list.append(l_row_dict)
        for row in data2:
            l_row_dict = row
            data_list2.append(l_row_dict)

        for row in data3:
            l_row_dict = row
            # Supongamos que el campo 'mul_archivo' es la URL de la imagen.
            # Si el archivo no está presente o está vacío, agregamos el flag has_valid_image como False.
            if not l_row_dict.get('mul_archivo'):
                l_row_dict['has_valid_image'] = False
            else:
                l_row_dict['has_valid_image'] = True
            data_list3.append(l_row_dict)
            # Se trabaja con el data_list
    rand_num = random.randrange(100000, 9999999)
    # sesion = int(request.GET['ses'])
    # print('SESIOOON ', sesion)
    context = {'segment': 'temas',
               'tema': data_list,
               'asi':data_list2,
               'redes': redes,
               'contact': contact,
               'random': rand_num,
               'multimedia': data_list3,
               'media_url': settings.MEDIA_URL
               }
               # 'random': sesion}

    html_template = loader.get_template('home/temas.html')
    return HttpResponse(html_template.render(context, request))

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def temas_por_asignatura(request):
    asi_id = request.GET.get('asi_id')
    searchTerm = request.GET.get('searchTerm', '')
    data_list = []

    with connection.cursor() as cursor:
        query = """SELECT 
                t.*, 
                a.asi_nombre, 
                COUNT(ta.tem_id) as numero_de_actividades,
                COALESCE(gm.mul_archivo, '/../static/img/Img-Template/classes-1.jpg') AS tema_imagen_url
            FROM gen.tema t
            JOIN gen.asignatura a ON t.asi_id = a.asi_id
            LEFT JOIN gen.tema_actividad ta ON t.tem_id = ta.tem_id
            LEFT JOIN gen.multimedia gm ON t.tem_id = gm.tem_id AND gm.act_id IS NULL AND gm.jue_id IS NULL AND gm.res_id IS NULL
            WHERE t.tem_estado = %s"""
        params = ['1']
        if asi_id:
            query += " AND t.asi_id = %s"
            params.append(asi_id)

        if searchTerm:
            query += " AND t.tem_nombre ILIKE %s OR t.tem_descripcion ILIKE %s"
            params.extend([f"%{searchTerm}%", f"%{searchTerm}%"])

        query += " GROUP BY t.tem_id, a.asi_nombre, gm.mul_archivo ORDER BY t.tem_id;"

        cursor.execute(query, params)
        data = dictfetchall(cursor)
        for row in data:
            data_list.append(row)
    return JsonResponse(data_list, safe=False)

def get_asi(_request, asi_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT 
    t.*, 
    a.asi_nombre, 
    COUNT(ta.tem_id) as numero_de_actividades,
    COALESCE(gm.mul_archivo, '/../static/img/Img-Template/classes-1.jpg') AS tema_imagen_url
FROM gen.tema t
JOIN gen.asignatura a ON t.asi_id = a.asi_id
LEFT JOIN gen.tema_actividad ta ON t.tem_id = ta.tem_id
LEFT JOIN gen.multimedia gm ON t.tem_id = gm.tem_id AND gm.act_id IS NULL AND gm.jue_id IS NULL AND gm.res_id IS NULL
WHERE t.tem_estado = %s AND t.asi_id = %s
GROUP BY t.tem_id, a.asi_nombre, gm.mul_archivo
ORDER BY t.tem_id;""",
            ('1', asi_id))

        data = dictfetchall(cursor)
    response_data = {'message': "Success", 'temas': data} if data else {'message': "Not Found"}

    return JsonResponse(response_data)
def get_tact(_request,tem_id):
    temas=list(Gen_TemaActividad.objects.filter(tem_id=tem_id,tac_estado=1).values())
    if (len(temas) > 0):
        data = {'message': "Success", 'temas': temas}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_actividades(_request,act_id):
    actividad=list(Gen_Actividad.objects.filter(act_id=act_id,act_estado=1).values())
    if (len(actividad) > 0):
        data = {'message': "Success", 'actividad': actividad}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def get_Tmult(_request,tem_id):
    multimedia = list(Gen_Multimedia.objects.filter(tem_id=tem_id,act__isnull=True,res__isnull=True,jue__isnull=True).values())
    if (len(multimedia) > 0):
        data = {'message': "Success", 'multimedia': multimedia}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_Amult(_request):
    temas = list(Gen_Multimedia.objects.filter(res__isnull=True,jue__isnull=True).values())
    if (len(temas) > 0):
        data = {'message': "Success", 'multimedia': temas}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)




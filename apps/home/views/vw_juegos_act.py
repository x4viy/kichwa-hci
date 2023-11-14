
import random
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.gen.models import *
from django.http import JsonResponse
# @login_required(login_url="/login/")
from utils.utils import dictfetchall
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404
from apps.sis.models import *
from django.http import Http404, HttpResponse
def dictfetchall(cursor):
    "Devuelve todos los registros del cursor como un diccionario"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def juegos_act(request, tem_id,act_id):
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    with connection.cursor() as cursor:
        cursor.execute(
            """select * from gen.tema_actividad 
               where tem_id = %s and act_id = %s""",
            (tem_id, act_id)
        )
        tema_actividad = dictfetchall(cursor)
        if not tema_actividad:
            raise Http404("No Gen_TemaActividad matches the given query.")
        tac_id = tema_actividad[0]['tac_id']

        # Consulta para obtener los datos de Gen_Juego relacionados con el tac_id
        cursor.execute(
            """select gj.*, gt.tip_id 
               from gen.juego gj 
               join gen.tipo gt on gj.tip_id = gt.tip_id
               where gj.tac_id = %s and gj.jue_estado = %s""",
            (tac_id,'1')
        )
        gen_juegos = dictfetchall(cursor)
        for juego in gen_juegos:
            # Consulta para obtener mul_archivo de gen.multimedia basado en tip_id
            cursor.execute(
                """select mul_archivo 
                   from gen.multimedia 
                   where tip_id = %s
                   limit 1""",
                (juego['tip_id'],)
            )
            multimedia = cursor.fetchone()  # Obtenemos solo un resultado
            if multimedia:
                juego['mul_archivo'] = multimedia[0]
            else:
                juego['mul_archivo'] = '/../static/img/Img-Template/classes-1.jpg'



        cursor.execute(
            """select * from gen.multimedia m 
               where  m.mul_estado  = %s
               order by m.mul_id""",
            ('1'))

        # el resultado de la consulta se lo transforma a lista de diccionarios
        data2 = dictfetchall(cursor)
        data_list2 = []

        cursor.execute(
            """select * from gen.asignatura a 
               where  a.asi_estado  = %s""",
            ('1'))
        data3 = dictfetchall(cursor)
        data_list3 = []

        # Se trabaja con el data_list
        for row in data2:
            l_row_dict = row
            data_list2.append(l_row_dict)
            # Se trabaja con el data_list
        for row in data3:
            l_row_dict = row
            data_list3.append(l_row_dict)

    try:
        actividad = Gen_Actividad.objects.get(act_id=act_id)
        nombre_actividad = actividad.act_nombre  # Reemplaza 'nombre' con el nombre real del campo si es diferente
    except Gen_Actividad.DoesNotExist:
        nombre_actividad = None  # Puedes manejar el error como mejor te parezca

    # # Realiza la consulta a la tabla Gen_TemaActividad y obtiene los datos filtrando por tem_id
    # # Realiza la consulta al modelo Gen_TemaActividad para obtener los datos filtrando por tem_id y act_id
    # tema_actividad = get_object_or_404(Gen_TemaActividad, tem=tem_id, act=act_id)
    #
    # # Obtenemos los datos de Gen_Juego relacionados con el tact_id del tema_actividad
    # gen_juegos = Gen_Juego.objects.filter(tac=tema_actividad.tac_id).select_related('tip')

    context = {
        'segment': 'juegos_act',
        'tema_actividad': tema_actividad,
        'gen_juegos': gen_juegos,
        'multimedia': data_list2,
        'asi': data_list3,
        'redes': redes,
        'contact': contact,
        'media_url': settings.MEDIA_URL,
        'act_nombre': nombre_actividad,
        'tem_id': tem_id,
        'act_id': act_id
    }

    html_template = loader.get_template('home/juegos_act.html')
    return HttpResponse(html_template.render(context, request))

def juegos_busqueda(request, tem_id, act_id):
    searchTerm = request.GET.get('searchTerm', '')

    with connection.cursor() as cursor:
        cursor.execute(
            """select * from gen.tema_actividad 
               where tem_id = %s and act_id = %s""",
            (tem_id, act_id)
        )
        tema_actividad = dictfetchall(cursor)

        if not tema_actividad:
            raise Http404("No Gen_TemaActividad matches the given query.")
        tac_id = tema_actividad[0]['tac_id']

        # Consulta para obtener los datos de Gen_Juego relacionados con el tac_id
        base_query = """
            select gj.*, gt.tip_id 
            from gen.juego gj 
            join gen.tipo gt on gj.tip_id = gt.tip_id
            where gj.tac_id = %s and gj.jue_estado = %s
        """
        params = [tac_id, '1']

        # Añadir filtros si hay searchTerm
        if searchTerm:
            base_query += " AND (gj.jue_nombre ILIKE %s OR gj.jue_descripcion ILIKE %s)"
            params.extend([f"%{searchTerm}%", f"%{searchTerm}%"])

        cursor.execute(base_query, params)
        gen_juegos = dictfetchall(cursor)
        for juego in gen_juegos:
            # Consulta para obtener mul_archivo de gen.multimedia basado en tip_id
            cursor.execute(
                """select mul_archivo 
                   from gen.multimedia 
                   where tip_id = %s
                   limit 1""",
                (juego['tip_id'],)
            )
            multimedia = cursor.fetchone()  # Obtenemos solo un resultado
            if multimedia:
                juego['mul_archivo'] = multimedia[0]
            else:
                juego['mul_archivo'] = '/../static/img/Img-Template/classes-1.jpg'

    return JsonResponse(gen_juegos, safe=False)


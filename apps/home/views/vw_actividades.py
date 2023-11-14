# Autor: Bryan Amaya
import self
from django.db import connection
from django.http import HttpResponse
from django.template import loader
from apps.sis.models import *
# @login_required(login_url="/login/")
from core.encryption_util import EncryptDES
from utils.utils import dictfetchall
from django.conf import settings
import random
_e = EncryptDES()
from django.http import JsonResponse
def actividades(request,tem_id):
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    with connection.cursor() as cursor:
        query = """
                WITH ConteoJuegos AS (
    SELECT 
        t.tac_id,
        COUNT(j.tac_id) AS conteo_tac_id
    FROM gen.tema_actividad t 
    LEFT JOIN gen.juego j ON t.tac_id = j.tac_id
    WHERE t.tem_id = %s AND t.tac_estado = %s
    GROUP BY t.tac_id
)

SELECT 
    a.*, 
    COALESCE(c.conteo_tac_id, 0) AS conteo_tac_id,  -- Aquí se aplica COALESCE
    COALESCE(gm.mul_archivo, '/../static/img/Img-Template/classes-1.jpg') AS actividad_imagen_url
FROM gen.actividad a
JOIN gen.tema_actividad t ON a.act_id = t.act_id AND t.tem_id = %s  AND a.act_estado = %s
LEFT JOIN ConteoJuegos c ON t.tac_id = c.tac_id
LEFT JOIN gen.multimedia gm ON a.act_id = gm.act_id AND gm.tem_id IS NULL AND gm.jue_id IS NULL AND gm.res_id IS NULL
ORDER BY a.act_nombre ASC;
                """
        params = [tem_id, '1', tem_id, '1']
        cursor.execute(query, params)
        data = dictfetchall(cursor)
        data_list = []
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

        # Se tranfosrma de lista de diccionarios a JSON
        for row in data:
            l_row_dict = row
            data_list.append(l_row_dict)

        # Se trabaja con el data_list
        for row in data2:
            l_row_dict = row
            data_list2.append(l_row_dict)
            # Se trabaja con el data_list
        for row in data3:
            l_row_dict = row
            data_list3.append(l_row_dict)
    rand_num = random.randrange(100000, 9999999)
    context = {'segment': 'actividades',
               'actividad': data_list,
               'multimedia': data_list2,
               'asi': data_list3,
               'redes': redes,
               'contact': contact,
               'media_url': settings.MEDIA_URL,
               'tem_id': tem_id
               }

    html_template = loader.get_template('home/actividades.html')
    return HttpResponse(html_template.render(context, request))

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def actividad_busqueda(request, tem_id):
    searchTerm = request.GET.get('searchTerm', '')
    data_list = []

    base_query = """
        WITH ConteoJuegos AS (
            SELECT 
                t.tac_id,
                COUNT(j.tac_id) AS conteo_tac_id
            FROM gen.tema_actividad t 
            LEFT JOIN gen.juego j ON t.tac_id = j.tac_id
            WHERE t.tem_id = %s AND t.tac_estado = %s
            GROUP BY t.tac_id
        )

        SELECT 
            a.*, 
            COALESCE(c.conteo_tac_id, 0) AS conteo_tac_id,  -- Aquí se aplica COALESCE
            COALESCE(gm.mul_archivo, '/../static/img/Img-Template/classes-1.jpg') AS actividad_imagen_url
        FROM gen.actividad a
        JOIN gen.tema_actividad t ON a.act_id = t.act_id AND t.tem_id = %s  AND a.act_estado = %s
        LEFT JOIN ConteoJuegos c ON t.tac_id = c.tac_id
        LEFT JOIN gen.multimedia gm ON a.act_id = gm.act_id AND gm.tem_id IS NULL AND gm.jue_id IS NULL AND gm.res_id IS NULL
    """

    params = [tem_id, '1', tem_id, '1']

    if searchTerm:
        base_query += " WHERE (a.act_nombre ILIKE %s OR a.act_descripcion ILIKE %s)"
        params.extend([f"%{searchTerm}%", f"%{searchTerm}%"])

    base_query += " ORDER BY a.act_nombre ASC"

    with connection.cursor() as cursor:
        cursor.execute(base_query, params)
        data = dictfetchall(cursor)
        for row in data:
            data_list.append(row)

    return JsonResponse(data_list, safe=False)

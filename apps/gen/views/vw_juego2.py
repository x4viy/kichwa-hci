# Autor: Bryan Amaya
from django.db import connection
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import Template, Context, RequestContext
from django.template import loader

from utils.utils import dictfetchall


# def Juego1(request):
#     return render(request, 'juego1.html')

def Juego2(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """select '{'||
                '"titulo": ["'|| af.act_nombre ||'"] , '||
                '"alternativas": ['||(select STRING_AGG('"'||r.res_respuesta,'", ')
                                     from gen.respuesta r, gen.actividad a
                                     where r.act_id = af.act_id
                                     group by a.act_id 
                                     order by a.act_id LIMIT 1
                                    )||'"], '
                '"correcta": ["'||(select STRING_AGG(r.res_respuesta,'", ')
                              from gen.respuesta r, gen.actividad a
                              where r.res_escorrecta='true' and r.act_id=af.act_id
                              group by a.act_id 
                              order by a.act_id LIMIT 1)
                ||'"]}' as resultado
            from gen.actividad af
            where af.tem_id = %s
            order by af.act_id""",
            (str(request.GET['act'])))
        # where
        # res_estado = % s
        # el resultado de la consulta se lo transforma a lista de diccionarios
        data = dictfetchall(cursor)
        cursor.execute(
            """select af.act_puntaje as puntajepregunta
                from gen.actividad af
                where af.tem_id = %s
                order by af.act_id""",
            (str(request.GET['act'])))
        # where
        # res_estado = % s
        # el resultado de la consulta se lo transforma a lista de diccionarios
        data2 = dictfetchall(cursor)

    data_list = []
    # Se tranfosrma de lista de diccionarios a JSON
    for row in data:
        l_row_dict = row
        data_list.append(l_row_dict)
    for row in data2:
        l_row_dict = row
        data_list.append(l_row_dict)
    context = {'segment': 'juego2', 'datos': data, 'datos2':data2}
    html_template = loader.get_template('../templates/actividad_b/juego2.html')
    return HttpResponse(html_template.render(context, request))

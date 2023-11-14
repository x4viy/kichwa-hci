# Autor: Bryan Amaya

import random
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# @login_required(login_url="/login/")
from utils.utils import dictfetchall


def asignatura(request):

    with connection.cursor() as cursor:
        # Se genera el cursos con el SQL para realizar la consulta
        # cursor.execute(
        #     """select * from gen.tema t where t.tem_estado = %s order by t.tem_id""",
        #     ('1'))

        cursor.execute(
            """select * from gen.asignatura a where a.asi_estado = %s order by a.asi_id""",
            ('1'))

        # el resultado de la consulta se lo transforma a lista de diccionarios
        data = dictfetchall(cursor)


        data_list = []
        # Se tranfosrma de lista de diccionarios a JSON
        for row in data:
            l_row_dict = row
            data_list.append(l_row_dict)
            # Se trabaja con el data_list

    rand_num = random.randrange(100000, 9999999)

    # context2 = {'random': rand_num}
    context = {'segment': 'asignaturas',
               'asignatura': data_list,
               'random': rand_num}
    html_template = loader.get_template('home/asignatura.html')
    return HttpResponse(html_template.render(context, request))
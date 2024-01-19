# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Vista para la opción opcion.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar


from django.db import connection
from django.template import loader
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from apps.gen.forms import *
from django.http import HttpResponse, JsonResponse
from core.encryption_util import *

from django.shortcuts import redirect

_e = EncryptDES()

# Autor: Kevin Campoverde
class MultimediaGame(ListView):


    # Autor: Kevin Campoverde
    def myFirstView (request):
        # Se establece la conección a la base de datos
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                    FROM gen.carta c 
                    INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                    INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                    INNER JOIN gen.carta_sesion cs ON cs.case_cart_id = c.cart_id 
                    INNER JOIN gen.sesion_juego sj ON sj.seju_id =cs.case_seju_id 
                    WHERE c.cart_estado = 1 and sj.seju_estado =1
                    """,
                )

            data = dictfetchall(cursor)

        for i in data:
            i['descripcion'] = i['descripcion'].replace(' ', '-')

        context = {'segment': 'Juego de Memoria', 'datos': data }
        print('datitos ', data)
        # html_template = loader.get_template('home/juego1.html')
        html_template = loader.get_template('../templates/Juegos-Multimedia/memory-game_connection_with_db.html')
        return HttpResponse(html_template.render(context, request))
        #return render(request, 'Juegos-Multimedia/memory-game_connection_with_db.html')

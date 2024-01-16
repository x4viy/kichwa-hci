from django.shortcuts import render
from django.db import connection
from apps.gen.forms import *

# Create your views here.
# Create your views here.
def index(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                FROM gen.carta c 
                INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                WHERE c.cart_estado = 1
                """,
        )

        data = dictfetchall(cursor)

    for i in data:
        i['descripcion'] = i['descripcion'].replace(' ', '-')
    data[0]["url"] = "url de carta"
    context = {'segment': 'Juego de Memoria', 'datos': data }
    return render(request, 'Juegos-Multimedia/clasification-game.html', context)
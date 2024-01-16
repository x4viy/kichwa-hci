from typing import List, Dict, Any

from django.shortcuts import render
from django.db import connection
from apps.gen.forms import *


# Cards to be displayed in the game by session code
def index(request):
    # TODO: Get the code from the request
    cards = get_session_cards("123456")
    info = get_session_info("123456")
    context = {'segment': 'Juego de Memoria', 'cards': cards, 'info': info}
    return render(request, 'Juegos-Multimedia/clasification-game.html', context)


def get_session_cards(session_code):
    '''
    Get cards to be displayed in the game by session code
    :param session_code:
    :return: list[dict[Any, Any]]
    '''
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                FROM gen.carta c 
                INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                WHERE c.cart_estado = 1
                """,
        )

        cards = dictfetchall(cursor)

    for i in cards:
        i['descripcion'] = i['descripcion'].replace(' ', '-')
    return cards


def get_session_info(session_code):
    '''
    Get the socket url introduction
    :param session_code:
    :return: list[dict[Any, Any]]
    '''
    #TODO: Get the info from the database
    info = {"code": session_code , "introduction": "Bienvenido al juego de clasificación"}
    return info


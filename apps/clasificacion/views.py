import random
from typing import List, Dict, Any

from django.shortcuts import render
from django.db import connection
from apps.gen.forms import *
from utils.utils import get_ip_address


# Cards to be displayed in the game by session code
def index(request):
    # TODO: Get the code and name from the request
    cards = get_session_cards("123456")
    info = get_session_info("123456", "Antonio")
    options = get_option_cards(cards);
    context = {'segment': 'Juego de Clasificacion',
               'cards': cards,
               'options': options,
               'info': info
               }
    return render(request, 'Juegos-Multimedia/clasification-game.html', context)


def get_session_cards(session_code):
    '''
    Get cards to be displayed in the game by session code
    :param session_code:
    :return: list[dict[Any, Any]]
    '''
    # TODO: Get the category of card and append / search from the options names in the database
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT c.cart_id as ID, c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                FROM gen.carta c 
                INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                WHERE c.cart_estado = 1
                """,
        )

        cards = dictfetchall(cursor)

    # simula establecer las opciones de cada carta (2 posibles)

    return cards


def get_option_cards(cards):
    """
    Get the options of the cards
    :param cards:
    :return: list[dict[Any, Any]]
    """
    options = []
    for index, item in enumerate(cards):
        rand_indices = card_rand_options(index, len(cards))
        options.append([cards[rand_indices[0]]['descripcion'], cards[rand_indices[1]]['descripcion']])
    return options


def get_session_info(session_code, name):
    """
    Get the socket url introduction
    :param session_code:
    :return: list[dict[Any, Any]]
    """
    # TODO: Get the info from the database
    current_ip = get_ip_address()
    info = {
        'url_socket': 'ws://' + current_ip + ':8000/ws/classification/' + session_code + name + '/',
        'session_code': session_code,
        'name': name
    }

    return info


def card_rand_options(actual, total):
    """
    Method to generate a random number that is different from the current one
    :param actual: current number
    :param total: total number of cards
    :return: list [int, int]
    """
    if total <= 1:
        raise ValueError("Total must be greater than 1")

    valor_aleatorio = random.choice([i for i in range(total) if i != actual])
    lista = [actual, valor_aleatorio]
    random.shuffle(lista)
    return lista

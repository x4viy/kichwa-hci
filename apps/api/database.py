from django.db import connection

from apps.clasificacion.models import get_session_info, get_option_cards
from apps.gen.models import PreInfoSession
from utils.utils import *


def is_code_in_db(code):
    """
    Get the code of the session from the database
    :param code:
    :return: true if the code is in the database, false otherwise
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT s.seju_codigo AS CODEGAME 
                FROM gen.sesion_juego s 
                WHERE s.seju_codigo = %s
                """,
            [code],
        )

        data = dictfetchall(cursor)
        if data:
            return True
        return False


def get_game_intro(code):
    """
    Get the session intro from the database
    :param code:
    :return: the session intro
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT s.seju_introduccion AS INTROGAME
                FROM gen.sesion_juego s 
                WHERE s.seju_codigo = %s
                """,
            [code],
        )

        data = dictfetchall(cursor)
        if data:
            return data[0]['introgame']
        return None


def save_info_session(code):
    """
    Get the session information from the database
    :param code:
    :return: the session information
    """


def get_session_cards(session_code):
    """
    Get cards to be displayed in the game by session code
    :param session_code:
    :return: list[dict[Any, Any]] or None if there are no cards
    """
    # TODO: Get the category of card and append / search from the options names in the database
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT c.cart_id as ID,  c.cart_descripcion AS DESCRIPCION, c.cart_traduccion as TRADUCCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                FROM gen.carta c 
                INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id =c.cart_id 
                INNER JOIN gen.cart_cate_sesion ccs ON ccs.ccs_carca_id  = cc.carca_id  
                INNER JOIN gen.sesion_juego sj ON sj.seju_id =ccs.ccs_seju_id 
                WHERE c.cart_estado = 1 and sj.seju_estado =1 and sj.seju_codigo = %s
                """,
            [session_code],
        )

        cards = dictfetchall(cursor)
    if not cards:
        return None

    for i in cards:
        i['descripcion'] = i['descripcion'].replace(' ', '-')

    # Group the cards by the ID of the card
    cards = _group_cards(cards)
    return cards


def _group_cards(cards):
    """
    Group the cards by the ID of the card as key of its own dictionary and as a value a list of the rest of the data, for the type create a a list with  the [0] all the data with info the card containing card with the Tipo as 'imagen' and in the [1] all the data with info the card containing card with the Tipo as 'audio'
    :param cards:
    :return: dict[dict[Any, Any], list[list[dict[Any, Any]], list[dict[Any, Any]]]]
    """
    cards_grouped = {}
    for card in cards:
        card_id = str(card['id'])
        if card_id not in cards_grouped:
            cards_grouped[card_id] = {
                'id': card['id'],
                'descripcion': card['descripcion'],
                'traduccion': card['traduccion'],
                'image': None,
                'audio': None
            }
        if card['tipo'] == 'image':
            cards_grouped[card_id]['image'] = card['ruta']
        elif card['tipo'] == 'audio':
            cards_grouped[card_id]['audio'] = card['ruta']

    return cards_grouped


def get_games_with_phone_connection():
    """
    Get the games code that can be played with phone connection (qr)
    :return:
    """
    return ['6']


def need_qr(code):
    """
    Get the games code that can be played with phone connection (qr)
    :return:
    """
    if get_game_type(code) in get_games_with_phone_connection():
        return True
    return False


def get_game_type(code):
    """
    Get the game type from the database
    :param code:
    :return: the game type
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT t.tip_codigo AS TYPEGAME
                FROM gen.tipo t
                INNER JOIN gen.sesion_juego s ON s.seju_tip_id = t.tip_id
                WHERE s.seju_codigo = %s
                """,
            [code],
        )

        data = dictfetchall(cursor)
        if data:
            return data[0]['typegame']
        return None

def is_token_active(token):
    """
    Verify in for given token if session is active
    :param token:
    :return: true if the session is active, false otherwise
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT p.is_active AS ACTIVE
                FROM gen.pre_info_session p
                WHERE p.csrf_token = %s
                """,
            [token],
        )

        data = dictfetchall(cursor)
        if data and data[0]['active']:
            return True
        return False

def set_token_active(token):
    """
    Set the token to active
    :param token:
    :return: true if the token was set to active, false otherwise
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """ UPDATE gen.pre_info_session p
                    SET is_active = true
                    WHERE p.csrf_token = %s
                    """,
                [token],
            )
            return True
        except Exception as e:
            return False

def get_session_info_by_token(token):
    """
    Get the session information from the database
    :param token:
    :return: the session information
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """ SELECT p.session_info AS INFO
                FROM gen.pre_info_session p
                WHERE p.csrf_token = %s
                """,
            [token],
        )

        data = dictfetchall(cursor)
        if data:
            return data[0]['info']
        return None

def get_game_data(session_code, name):
    """
    Get the game data from the database
    :param session_code:
    :param name:
    :return: dict[Any, Any] or None if there are no cards
    """
    cards = get_session_cards(session_code)
    info = get_session_info(session_code, name)
    options = get_option_cards(cards);
    context = {'segment': 'Juego de Clasificacion',
               'cards': cards,
               'options': options,
               'info': info
               }
    return context


def store_pre_session(token, data):
    """
    Store the pre session in the database for qr assosiated games
    :param token: str
    :param data:  Dict[Any, Any]
    :return: true if the pre session was stored, false otherwise
    """
    var = PreInfoSession()
    var.csrf_token = token
    var.session_info = data
    var.is_active = False
    var.save()

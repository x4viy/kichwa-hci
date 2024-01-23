from django.db import models
import random

from utils.utils import get_ip_address


# Create your models here.
def get_option_cards(cards):
    """
    Get the options of the cards
    :param cards:
    :return: list[dict[Any, Any]]
    """
    options = []
    cardsList = list(cards.values())
    for index, item in enumerate(cards):
        rand_indices = card_rand_options(index, len(cards))
        options.append([cardsList[rand_indices[0]]['traduccion'], cardsList[rand_indices[1]]['traduccion']])
    return options


def get_session_info(session_code, name):
    """
    Get the socket url introduction
    :param session_code:
    :param name:
    :return: list[dict[Any, Any]]
    """
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

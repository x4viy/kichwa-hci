import json
import random
from typing import List, Dict, Any

from django.shortcuts import render
from django.db import connection

from apps.api.database import get_session_cards
from apps.clasificacion.models import get_session_info, get_option_cards
from apps.gen.forms import *
from utils.utils import get_ip_address


# Cards to be displayed in the game by session code
def index(request):
    code = request.session.get('code')
    name = request.session.get('name')
    cards = get_session_cards(code)
    info = get_session_info(code, name)
    options = get_option_cards(cards);

    # cards_grouped_str_keys = {str(k): v for k, v in cards.items()}
    # cards_json = json.dumps(cards_grouped_str_keys)
    context = {'segment': 'Juego de Clasificacion',
               'cards': cards,
               'options': options,
               'info': info
               }
    return render(request, 'Juegos-Multimedia/clasification-game.html', context)





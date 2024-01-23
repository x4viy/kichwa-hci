import json
import random
from typing import List, Dict, Any

from django.shortcuts import render
from django.db import connection

from apps.api.database import get_session_cards, get_session_info_by_token
from apps.clasificacion.models import get_session_info, get_option_cards
from apps.gen.forms import *
from utils.utils import get_ip_address


# Cards to be displayed in the game by session code
def index(request, token):
    context = get_session_info_by_token(token)
    return render(request, 'Juegos-Multimedia/clasification-game.html', context)





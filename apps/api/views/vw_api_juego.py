# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Vista para la opción opcion.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar

import json
import django.db.models.query_utils
import pandas as pd
from django.db import transaction, connection
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.sis.models import *
from apps.sis.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from django.shortcuts import redirect
from vars.msg import CRUD_MSG



import json
import django.db.models.query_utils
import pandas as pd
from django.db import transaction, connection
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.gen.forms import *
from vars.js import datatable_opts

from core.encryption_util import *

from django.shortcuts import redirect

_e = EncryptDES()

# Autor: Kevin Campoverde
class MultimediaGame(ListView):


    # Autor: Kevin Campoverde
    def myFirstView (request):
        return render(request, 'Juegos-Multimedia/memory-game.html')


    def secondView (request):
        return render(request, 'Juegos-Multimedia/create-card.html')
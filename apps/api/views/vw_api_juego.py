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
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
import numpy as np
from django.shortcuts import redirect



from django.db import connection
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView

from apps.api.database import is_code_in_db
from apps.gen.forms import *
from django.http import HttpResponse, JsonResponse
from core.encryption_util import *

from django.shortcuts import redirect

_e = EncryptDES()


# Autor: Kevin Campoverde
class MultimediaGame(ListView):

    def code(request):
        """
        TODO: verify if code session exist
        Verify code
        """
        # context = {'segment': 'Juego de Memoria', 'datos': data }
        # html_template = loader.get_template('../templates/Juegos-Multimedia/memory-game_connection_with_db.html')
        # return HttpResponse(html_template.render(context, request))
        print('entro en code')
        # url_list = reverse('user_code')
        return render(request, 'Juegos-Multimedia/multimedia-code.html')

    def verify_code(request):
        """
        TODO: verify if code session exist
        Verify code
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request'})

        if not request.POST.get('code'):
            return JsonResponse({'message': 'Not field code'})

        code = request.POST.get('code')
        print('code: ', code)

        if not is_code_in_db(code):
            return JsonResponse({'message': 'No se encontro el códio de sesión'})

        # return reverse('user_code', args(code))
        # user_url = 'multimedia/user/'
        # return JsonResponse({'message': 'ok', 'url': user_url, 'code': code})
        # return JsonResponse({'message': 'ok', 'code': code})
        # return redirect('multimedia_game:user_code', code=code)
        user_url = reverse('multimedia_game:user_code', args=[code])
        return JsonResponse({'message': 'ok', 'url': user_url})

    def user_code(request, code):
        """
        Display qr code and socket url with code session and name user
        """

        print('user', code)

        # context = {'segment': 'Juego de Memoria', 'code': code, 'name': name}
        html_template = loader.get_template('Juegos-Multimedia/multimedia-user.html')
        context = {'segment': 'Juego de Memoria', 'code': code}
        # user_url = reverse('multimedia_game:intro', args=[code])
        # return JsonResponse({'message': 'ok', 'url': user_url, 'code': code, 'name': name})
        # return JsonResponse({'message': 'no'})
        return HttpResponse(html_template.render(context, request))

    def to_intro(request):
        """
        Register user and code session , next redirect to introduction game
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request user_code'})
        if not request.POST.get('code') and not request.POST.get('name'):
            return JsonResponse({'message': 'No existe el usuario o el código de sesión'})
        print('intro', request.POST.get('name'))
        # TODO: GET THE INTRO OF THE SESSION
        intro = 'Este es el intro del juego de cartas consultado en la base de datos con el codigo de sesion y el nombre del usuario'
        name = request.POST.get('name')
        enc_code = request.POST.get('code')
        user_url = reverse('multimedia_game:intro', args=[enc_code, name, intro])
        return JsonResponse({'message': 'ok', 'url': user_url})

    def intro(request, code, name, text_intro):
        """
        Display qr code and socket url with code session and name user
        """
        print('code', code)
        print('user', name)
        # context = {'segment': 'Juego de Memoria', 'code': code, 'name': name}
        html_template = loader.get_template('Juegos-Multimedia/multimedia-intro.html')
        context = {'segment': 'Juego de Memoria', 'code': code, 'name': name, 'intro': text_intro}
        # user_url = reverse('multimedia_game:intro', args=[code])
        # return JsonResponse({'message': 'ok', 'url': user_url, 'code': code, 'name': name})
        # return JsonResponse({'message': 'no'})
        return HttpResponse(html_template.render(context, request))

    def check_phone_connection(request):
        """
        Check if the phone is connected to the socket
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request'})
        if not request.POST.get('code') and not request.POST.get('code'):
            return JsonResponse({'message': 'Not field code'})
        code = request.POST.get('code')
        name = request.POST.get('username')
        print('check', code, name)
        return JsonResponse({'message': 'ckeck'})
        # context = {'segment': 'Juego de Memoria', 'code': code, 'name': name}
        # html_template = loader.get_template('Juegos-Multimedia/multimedia-intro.html')
        # return HttpResponse(html_template.render(context, request))

    # Autor: Kevin Campoverde
    def myFirstView(request):
        # Se establece la conección a la base de datos
        print('tas aqui')

        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, ma.muar_tipo AS TIPO
                    FROM gen.carta c 
                    INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                    INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                    INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id =c.cart_id 
                    INNER JOIN gen.cart_cate_sesion ccs ON ccs.ccs_carca_id  = cc.carca_id  
                    INNER JOIN gen.sesion_juego sj ON sj.seju_id =ccs.ccs_seju_id 
                    WHERE c.cart_estado = 1 and sj.seju_estado =1
                    """,
            )

            data = dictfetchall(cursor)

        for i in data:
            i['descripcion'] = i['descripcion'].replace(' ', '-')

        context = {'segment': 'Juego de Memoria', 'datos': data}
        print('datitos ', data)
        # html_template = loader.get_template('home/juego1.html')
        html_template = loader.get_template('../templates/Juegos-Multimedia/memory-game_connection_with_db.html')
        return HttpResponse(html_template.render(context, request))
        # return render(request, 'Juegos-Multimedia/memory-game_connection_with_db.html')

    def secondView(request):
        return render(request, 'Juegos-Multimedia/memory-game.html')


    def classification_info(request):
        return render(request, 'Juegos-Multimedia/memory-game.html')

    def test(request):
        return render(request, 'Juegos-Multimedia/-game.html')

    def clasification_game_view(request):
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

        context = {'segment': 'Juego de Memoria', 'datos': data}
        html_template = loader.get_template('../templates/Juegos-Multimedia/clasification-game.html')
        return HttpResponse(html_template.render(context, request))
        # return render(request, 'Juegos-Multimedia/clasification-game.html')

    class SessionGame(ListView):
        """
        Contains methods to handle the game session
        """

        def get_sessoin_info(self, request):
            """
            Get the session information from the database

            :param request:
            :return: list[dict['url_socket', Any], [dict['options', Any], [dict['cards', Any]]
            """
            # TODO: Get the session info from the database
            session_info = {"url_socket": "ws://localhost:8000/ws/chat/123456/"}

            return JsonResponse(session_info)

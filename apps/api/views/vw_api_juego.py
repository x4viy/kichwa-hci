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
from django.views.decorators.csrf import csrf_exempt
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

from apps.api.database import *
from apps.gen.forms import *
from django.http import HttpResponse, JsonResponse
from core.encryption_util import *

from django.shortcuts import redirect

_e = EncryptDES()


# Autor: Kevin Campoverde
class MultimediaGame(ListView):

    def code(request):
        """
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
        Verify code
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Solictud no válida'})

        if not request.POST.get('code'):
            return JsonResponse({'message': 'No existen campos en el formulario'})

        code = request.POST.get('code')
        print('verify_code: ', code)

        if not is_code_in_db(code):
            return JsonResponse({'message': 'No se encontró el código de sesión'})

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
        if not request.POST.get('code') and not request.POST.get('name') and not request.POST.get('token'):
            return JsonResponse({'message': 'No existe el usuario o el código de sesión'})
        enc_code = request.POST.get('code')
        intro = get_game_intro(enc_code)
        name = request.POST.get('name')
        request.session['intro'] = intro
        request.session['name'] = name
        request.session['code'] = enc_code
        token = request.POST.get('token')
        # Verify the type of game session by the code session
        if need_qr(enc_code):
            data = get_game_data(enc_code, name)
            store_pre_session(token, data)
        user_url = reverse('multimedia_game:intro', args=[token])
        return JsonResponse({'message': 'ok', 'url': user_url})

    def intro(request, token):
        """
        Display qr code (byGame) and socket url with code session and name user
        """
        code = request.session.get('code')
        name = request.session.get('name')
        intro = request.session.get('intro')
        # Add url and  qr_code and encode the concatenation of both
        encoded_info = ''
        if need_qr(code):
            encoded_info = base64.b64encode((get_url_active() + '|' + token).encode('utf-8')).decode('utf-8')
        html_template = loader.get_template('Juegos-Multimedia/multimedia-intro.html')
        context = {'segment': 'Juego de Memoria', 'code': code, 'name': name, 'intro': intro, 'qr_code': encoded_info}
        return HttpResponse(html_template.render(context, request))

    def to_game(request):
        """
        Retrieve the game url by the code session
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request user_code'})
        if not request.POST.get('code') and not request.POST.get('name'):
            return JsonResponse({'message': 'No existe el usuario o el código de sesión'})
        code = request.POST.get('code')
        name = request.POST.get('name')
        session_type = get_game_type(code)
        user_url = None
        if session_type == '5':
            user_url = reverse('multimedia_game:memory_game')
        if session_type == '6':
            user_url = reverse('multimedia_game:clasification_game')
        if user_url:
            return JsonResponse({'message': 'ok', 'url': user_url, 'code': code})
        return JsonResponse({'message': 'No existe el tipo de juego'})

    def check_phone_connection(request):
        """
        Check if the phone is connected to the socket by cheking the isActive field in the database
        for given token
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request'})
        if not request.POST.get('token'):
            return JsonResponse({'message': 'Not field token'})
        token = request.POST.get('token')
        if is_token_active(token):
            user_url = reverse('multimedia_game:clasification_game')
            return JsonResponse({'message': 'ok', 'url': user_url})
        return JsonResponse({'message': 'Sin cambio'})

    @csrf_exempt
    def set_active(request):
        """
        Set active the session by the token
        """
        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request'})
        if not json.loads(request.body).get('token'):
            return JsonResponse({'message': 'Not field token'})
        token = json.loads(request.body).get('token')
        if set_token_active(token):
            info = get_session_info_by_token(token)
            return JsonResponse({'message': 'ok', 'info': info})
        return JsonResponse({'message': 'Sin cambio'})

    # Autor: Kevin Campoverde
    def memory(request):
        code = request.session.get('code')
        name = request.session.get('name')
        # Se establece la conección a la base de datos
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

        context = {'segment': 'Juego de Memoria',
                   'datos': data,
                   'code': code,
                   'name': name
                   }
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


def get_url_active():
    return 'http://' + get_ip_address() + ':8000/500/multimedia/active/'

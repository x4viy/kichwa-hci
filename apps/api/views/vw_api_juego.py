# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Vista para la opción opcion.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar
import json

from certifi.__main__ import args
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

    # function routes
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
        return render(request, 'Juegos-Multimedia/multimedia-code.html', {'url_list': url_list})

    def verify_code(request):
        """
        TODO: verify if code session exist
        Verify code
        """
        print('entro en verify')

        if request.method != 'POST':
            return JsonResponse({'message': 'Not a POST request'})

        if not request.POST.get('code'):
            return JsonResponse({'message': 'Not field code'})

        code = request.POST.get('code')

        if not is_code_in_db(code):
            return JsonResponse({'message': 'No se encontro el códio de sesión'})

        # return reverse('user_code', args(code))
        # user_url = 'multimedia/user/'
        # return JsonResponse({'message': 'ok', 'url': user_url, 'code': code})
        # return JsonResponse({'message': 'ok', 'url': user_url, 'code': code})

    def user(request, code):
        """
        Register user and code session , next redirect to introduction game
        """
        # if request.method != 'POST':
        #     return JsonResponse({'message': 'Not a POST request'})

        # code = request.POST.get('code')
        # name = request.POST.get('name')
        print('user', code)
        return render(request, 'Juegos-Multimedia/multimedia-user.html')
        # return render(request, 'Juegos-Multimedia/multimedia-code.html')

    # Autor: Kevin Campoverde
    def myFirstView(request):
        # Se establece la conección a la base de datos
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

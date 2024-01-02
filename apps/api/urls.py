# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.api.views.vw_api_juego import *
from apps.api.views.vw_gen_juego_multimedia import *
from apps.api.handler_file import *
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path


app_name = 'multimedia_game'

urlpatterns = [
    # Autor: Kevin Campoverde
    # Fecha: 27/12/2022 16:00
    # Descripción: URLs para la opción 'Opcion'.
    path("multimedia/game/", MultimediaGame.myFirstView, name="multimedia_game"),

    path("carta/list/", login_required(Gen_CartaListView.as_view()), name="gen_carta_list"),
    path("carta/add/", login_required(Gen_CartaCreateView.as_view()), name="gen_carta_add"),
    path("carta/edit/<str:pk>/", login_required(Gen_CartaUpdateView.as_view()),
         name="gen_carta_edit"),

    path('upload_file/', upload_file, name='upload_file'),
    path('delete_file/', delete_file, name='delete_file'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

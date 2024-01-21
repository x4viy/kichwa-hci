# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.views.static import serve

from apps.api.views.vw_api_juego import *
from apps.api.views.vw_gen_juego_multimedia import *
from apps.api.handler_file import *
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include  # add this
from django.urls import path, re_path

app_name = 'multimedia_game'

urlpatterns = [
    # Autor: Kevin Campoverde
    # Fecha: 27/12/2022 16:00
    # Descripción: URLs para la opción 'Opcion'.

    # game code init
    # path("multimedia/code/", MultimediaGame.code, name="multimedia_code"),
    # path("multimedia/verify_code/", MultimediaGame.verify_code, name="multimedia_code"),
    # path("multimedia/user_code/<int:code>/", MultimediaGame.user, name="user_code"),

    # card memery game
    path("multimedia/game/", MultimediaGame.myFirstView, name="multimedia_game"),
    path("multimedia/game2/", MultimediaGame.secondView, name="multimedia_game2"),

    # classification game
    path('multimedia/classification/', include("apps.clasificacion.urls")),
    path('multimedia/classification_info/', MultimediaGame.classification_info, name="game_info"),

    path("carta/list/", login_required(Gen_CartaListView.as_view()), name="gen_carta_list"),
    path("carta/add/", login_required(Gen_CartaCreateView.as_view()), name="gen_carta_add"),
    path("carta/edit/<str:pk>/", login_required(Gen_CartaUpdateView.as_view()),
         name="gen_carta_edit"),

    path('upload_file/', upload_file, name='upload_file'),
    path('delete_file/', delete_file, name='delete_file'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.views.static import serve

from apps.api.views.vw_api_juego import *
from apps.api.views.vw_gen_juego_multimedia import *
from apps.api.views.vw_api_sesion_juego import *
from apps.api.views.vw_api_categoria import *
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
    path("multimedia/code/", MultimediaGame.code, name="multimedia_code"),
    path("multimedia/verify_code/", MultimediaGame.verify_code, name="multimedia_code"),
    path('multimedia/user_code/<str:code>/', MultimediaGame.user_code, name='user_code'),
    path('multimedia/to_intro/', MultimediaGame.to_intro, name='to_intro'),
    path('multimedia/intro/<str:code>/<str:name>/<str:text_intro>/', MultimediaGame.intro, name='intro'),
    path('multimedia/check/', MultimediaGame.check_phone_connection, name='check_phone_connection'),

    # card memory game
    path("multimedia/game/", MultimediaGame.myFirstView, name="multimedia_game"),

    # classification game
    path('multimedia/classification/<str:code>/<str:name>/', include("apps.clasificacion.urls")),
    path('multimedia/classification_info/', MultimediaGame.classification_info, name="game_info"),

    path("carta/list/", login_required(Gen_CartaListView.as_view()), name="gen_carta_list"),
    path("carta/add/", login_required(Gen_CartaCreateView.as_view()), name="gen_carta_add"),
    path("carta/edit/<str:pk>/", login_required(Gen_CartaUpdateView.as_view()),
         name="gen_carta_edit"),

    path("categoria/list/", login_required(Gen_CategoriaListView.as_view()), name="gen_categoria_list"),
    path("categoria/add/", login_required(Gen_CategoriaCreateView.as_view()), name="gen_categoria_add"),
    path("categoria/edit/<str:pk>/", login_required(Gen_CategoriaUpdateView.as_view()),
         name="gen_categoria_edit"),

    path("sesion-juego/list/", login_required(Gen_SesionJuegoListView.as_view()), name="gen_ses_jue_list"),
    path("sesion-juego/add/", login_required(Gen_SesionJuegoCreateView.as_view()), name="gen_ses_jue_add"),
    path("sesion-juego/edit/<str:pk>/", login_required(Gen_SesionJuegoUpdateView.as_view()),
         name="gen_ses_jue_edit"),

    path('upload_file/', upload_file, name='upload_file'),
    path('delete_file/', delete_file, name='delete_file'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

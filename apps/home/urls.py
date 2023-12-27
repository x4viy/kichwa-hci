# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
import apps.home.views.vw_home
import apps.home.views.vw_temas
from apps.gen.views.vw_juego1 import Juego1
from apps.home.views.vw_index import *
from apps.home.views.vw_actividades import *
from apps.home.views.vw_home import *
from apps.home.views.vw_contact import *
from apps.home.views.vw_nosotros import *
from apps.home.views.vw_temas import *
from apps.home.views.vw_juegos_act import *
from apps.home.views.vw_terminos import *
from apps.home.views.vw_gen_tipo1 import *
from django.urls import path
from apps.home.views.vw_panel import *
app_name = 'home'
urlpatterns = [

    # The home page
    path('', home, name='home'),
    # path('indexfinal/', indexfinal, name='indexfinal'),
    path('home/', home, name='home'),
    path('temas/', temas, name='temas'),
    path('temas/<int:asi_id>/', temas, name='temas'),
    path('contact/', contact, name='contact'),
    path('nosotros/', nosotros, name='nosotros'),
    path('terminos/', terminos, name='terminos'),
    path('perfil/', perfil, name='perfil'),
    path('actualizar_perfil/', actualizar_perfil, name='actualizar_perfil'),
    path('puntajes/', puntajes, name='puntajes'),
    path('actividades/<int:tem_id>/<int:act_id>/', juegos_act, name='juegos_act'),
    # path('list_temas/<int:cat_id>', apps.home.views.vw_home, name='get_temas'),
    path('list_asi/<int:asi_id>', apps.home.views.vw_temas.get_asi, name='get_asi'),
    path('list_tact/<int:tem_id>', apps.home.views.vw_temas.get_tact, name='get_tact'),
    path('list_act/<int:act_id>', apps.home.views.vw_temas.get_actividades, name='get_actividades'),
    path('list_mul/<int:tem_id>', apps.home.views.vw_temas.get_Tmult, name='get_Tmult'),

    path("actividades/<int:tem_id>/", actividades, name="actividades"),

    path("tipo/<int:tip_id>/<int:jue_id>/", tipo1, name="tipo1"),
    path('tipos/<str:json_data>/', jugar_todos, name='jugar_todos'),
    path('temas_por_asignatura/',temas_por_asignatura, name='temas_por_asignatura'),
    path("actividades_busqueda/<int:tem_id>/", actividad_busqueda, name='actividad_busqueda'),
    path("juegos_busqueda/<int:tem_id>/<int:act_id>/", juegos_busqueda, name='juegos_busqueda'),
    path('enviar_puntajes/', enviar_puntajes, name='enviar_puntajes'),

    # # Matches any html file
    # re_path(r'^.*\.*', pages, name='pages'),
    # re_path(r'^.*\.*', pages, name='pages'),
]

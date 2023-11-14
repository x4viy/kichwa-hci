# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
# ---------------------------------------------------------------
# Autor: Dre
# Fecha: 17/12/2022 09:00
# Descripción: URLs para el  modulo general.
# ---------------------------------------------------------------
"""
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path
from apps.gen.views.vw_gen_actividad import Gen_ActividadListView, Gen_ActividadUpdateView, Gen_ActividadCreateView, upload_file, delete_file
from apps.gen.views.vw_gen_juego import Gen_JuegoListView, Gen_JuegoUpdateView, Gen_JuegoCreateView
from apps.gen.views.vw_gen_asignatura import *
from apps.gen.views.vw_gen_puntaje import Gen_PuntajeListView, Gen_PuntajeCreateView, Gen_PuntajeUpdateView
from apps.gen.views.vw_gen_tema import Gen_TemaListView, Gen_TemaCreateView, Gen_TemaUpdateView
from apps.gen.views.vw_juego1 import Juego1
from apps.gen.views.vw_juego2 import Juego2
from apps.gen.views.vw_juego3 import Juego3
from apps.gen.views.vw_gen_tipo1 import *
from apps.gen.views.vw_gen_multimedia import *
from apps.gen.views.vw_gen_tipo import *
app_name = 'gen'

urlpatterns = [
    # Autor: Dre
    # Fecha: 17/12/2022 10:00
    # Descripción: URLs para la opción 'Asignaturas'.

    path("actividad/list/", login_required(Gen_ActividadListView.as_view()), name="gen_actividad_list"),
    path("actividad/add/", login_required(Gen_ActividadCreateView.as_view()), name="gen_actividad_add"),
    path("actividad/edit/<str:pk>/", login_required(Gen_ActividadUpdateView.as_view()),
         name="gen_actividad_edit"),

    path("asignatura/list/", login_required(Gen_AsignaturaListView.as_view()), name="gen_asignatura_list"),
    path("asignatura/add/", login_required(Gen_AsignaturaCreateView.as_view()), name="gen_asignatura_add"),
    path("asignatura/edit/<str:pk>/", login_required(Gen_AsignaturaUpdateView.as_view()),
         name="gen_asignatura_edit"),

    path("tema/list/", login_required(Gen_TemaListView.as_view()), name="gen_tema_list"),
    path("tema/add/", login_required(Gen_TemaCreateView.as_view()), name="gen_tema_add"),
    path("tema/edit/<str:pk>/", login_required(Gen_TemaUpdateView.as_view()),
         name="gen_tema_edit"),


    path("tipo/list/", login_required(Gen_TipoListView.as_view()), name="gen_tipo_list"),
    path("tipo/add/", login_required(Gen_TipoCreateView.as_view()), name="gen_tipo_add"),
    path("tipo/edit/<str:pk>/", login_required(Gen_TipoUpdateView.as_view()),
         name="gen_tipo_edit"),

    path("juego/list/", login_required(Gen_JuegoListView.as_view()), name="gen_juego_list"),
    path("juego/add/", login_required(Gen_JuegoCreateView.as_view()), name="gen_juego_add"),
    path("juego/edit/<str:pk>/", login_required(Gen_JuegoUpdateView.as_view()),
         name="gen_juego_edit"),

    path("multimedia/list/", login_required(Gen_MultimediaListView.as_view()), name="gen_multimedia_list"),
    path("multimedia/add/", login_required(Gen_MultimediaCreateView.as_view()), name="gen_multimedia_add"),
    path("multimedia/edit/<str:pk>/", login_required(Gen_MultimediaUpdateView.as_view()),
         name="gen_multimedia_edit"),

    path("puntaje/list/", login_required(Gen_PuntajeListView.as_view()), name="gen_puntaje_list"),
    path("puntaje/add/", login_required(Gen_PuntajeCreateView.as_view()), name="gen_puntaje_add"),
    path("puntaje/edit/<str:pk>/", login_required(Gen_PuntajeUpdateView.as_view()),
         name="gen_puntaje_edit"),
    path('upload_file/', upload_file, name='upload_file'),
    path('delete_file/', delete_file, name='delete_file'),
    path("actividad/1/", Juego1, name="juego1"),
    path("actividad/2/", Juego2, name="juego2"),
    path("actividad/3/", Juego3, name="juego3"),

    path("tipo/<int:tip_id>/<int:jue_id>/", tipo1, name="tipo1"),
    path('tipos/<str:json_data>/', jugar_todos, name='jugar_todos'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

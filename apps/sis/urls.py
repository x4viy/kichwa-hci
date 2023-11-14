# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from apps.sis.views.vw_sis_opcion import *
from apps.sis.views.vw_sis_informaciondetalle import *
from apps.sis.views.vw_sis_informacion import *
from apps.sis.views.vw_sis_rol import *
from apps.sis.views.vw_sis_usuario import *
app_name = 'sis'

urlpatterns = [
    # Autor: Bryan Amaya
    # Fecha: 19/12/2022 20:00
    # Descripción: URLs para la opción 'Opcion'.
    path("opcion/list/", Sis_OpcionListView.as_view(), name="sis_opcion_list"),
    path("opcion/add/", Sis_OpcionCreateView.as_view(), name="sis_opcion_add"),
    path("opcion/edit/<str:pk>/", Sis_OpcionUpdateView.as_view(),
         name="sis_opcion_edit"),
    
    path("informaciondetalle/list/", Sis_InformaciondetalleListView.as_view(), name="sis_informaciondetalle_list"),
    path("informaciondetalle/add/", Sis_InformaciondetalleCreateView.as_view(), name="sis_informaciondetalle_add"),
    path("informaciondetalle/edit/<str:pk>/", Sis_InformaciondetalleUpdateView.as_view(),
         name="sis_informaciondetalle_edit"),

    path("informacion/list/", Sis_InformacionListView.as_view(), name="sis_informacion_list"),
    path("informacion/add/", Sis_InformacionCreateView.as_view(), name="sis_informacion_add"),
    path("informacion/edit/<str:pk>/", Sis_InformacionUpdateView.as_view(),
         name="sis_informacion_edit"),
    
    path("rol/list/", login_required(Sis_RolListView.as_view()), name="sis_rol_list"),
    path("rol/add/", login_required(Sis_RolCreateView.as_view()), name="sis_rol_add"),
    path("rol/edit/<str:pk>/", login_required(Sis_RolUpdateView.as_view()),
         name="sis_rol_edit"),

    path("usuario/list/", login_required(Sis_UsuarioListView.as_view()), name="sis_usuario_list"),
    path("usuario/add/", login_required(Sis_UsuarioCreateView.as_view()), name="sis_usuario_add"),
    path("usuario/edit/<str:pk>/", login_required(Sis_UsuarioUpdateView.as_view()),
         name="sis_usuario_edit"),
]

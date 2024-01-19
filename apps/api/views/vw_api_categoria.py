# Autor: Bryan Amaya
# Fecha: 07/05/2023 17:00
# Descripción: Vista para la opción cabecera tema, detalle actividad.
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

#
_e = EncryptDES()


# Autor: Bryan Amaya
# Listar
class Gen_CategoriaListView(ListView):
    model = Gen_Categoria
    template_name = 'gen_juego/list.html'

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        usuario_actual = self.request.session['AIGN_USERID']
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual == 1:
            return Gen_Categoria.objects.all()
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_Categoria.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_Categoria.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name_plural
        context['url_form'] = reverse_lazy('multimedia_game:gen_categoria_add')  # add
        context['url_form_add'] = reverse_lazy('multimedia_game:gen_categoria_add')  # add
        context['url_form_edit'] = 'multimedia_game:gen_categoria_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'cat_nombre': None,
                                  'cat_descripcion': None,
                                }
        # encriptacion del id
        for r in context['object_list']:
            r.cat_id = _e.encrypt(r.cat_id)
        return context


# Autor: Bryan Amaya
# Agregar
class Gen_CategoriaCreateView(CreateView):
    model = Gen_Categoria
    form_class = Gen_CategoriaForm
    template_name = 'gen_categoria/create-categoria.html'
    success_url = reverse_lazy('multimedia_game:gen_categoria_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_CategoriaCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
    def get_initial(self):
        rol_id = self.request.session['AIGN_ROLID']
        usuario_id = self.request.session['AIGN_USERID']
        return {'rol_id': rol_id, 'usuario_id': usuario_id}

    # Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}
        print('ENTRE AL CREAR')

        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:

                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()

                messages.success(request, CRUD_MSG.CREATE)
                return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                print("error ", str(e))
                extra_errors.append(str(e))

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return JsonResponse(dict(form._errors.items()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        print('aaaaaqquii', context['url_list'])
        return context


# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_CategoriaUpdateView(UpdateView):
    model = Gen_Categoria
    form_class = Gen_CategoriaForm
    template_name = 'gen_categoria/create-categoria.html'
    success_url = reverse_lazy('multimedia_game:gen_categoria_list')

    def get(self, request, *args, **kwargs):
        print('aqui5')
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    # Autor: Bryan Amaya
    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        print('aqui6')
        kwargs = super(Gen_CategoriaUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    # Autor: Bryan Amaya
    def dispatch(self, request, *args, **kwargs):
        print('aqui7')
        # Desencriptando el pk
        for k in self.kwargs.keys():
            self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        print('aqui8')
        rol_id = self.request.session['AIGN_ROLID']
        usuario_id = self.request.session['AIGN_USERID']
        return {'rol_id': rol_id, 'usuario_id': usuario_id}

    #Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}

        print("adentro   ", request.POST)

        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:

                with transaction.atomic():
                    self.get_object().delete()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.utils.InternalError as e:
                extra_errors.append(str(e))

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return JsonResponse(dict(form.errors.items()))



    #Autor: Bryan Amaya
    def get_context_data(self, **kwargs):
        print('aqui9')
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        ret = []
        if 'pk' in context:
            cat_id = _e.decrypt(context['pk'])
        else:
            cat_id = context['object'].cat_id

        print('el cat_id', cat_id)

        return context

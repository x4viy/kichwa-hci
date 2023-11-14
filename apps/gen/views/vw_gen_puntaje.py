# Autor: emdr
# Fecha: 17/12/2022 010:00
# Descripción: Vista para la opción categorias.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar

import django.db.models.query_utils
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
from django.shortcuts import redirect
#
_e = EncryptDES()


# Listar
class Gen_PuntajeListView(ListView):
    model = Gen_Puntaje
    template_name = 'gen_puntaje/list.html'

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
        email_actual = self.request.session['AIGN_EMAIL']
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual == 1:
            return Gen_Puntaje.objects.all()
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_Puntaje.objects.filter(pun_emailprofesor=email_actual)
            # return Gen_Puntaje.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_Puntaje.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_puntaje_add') #add
        context['url_form_add'] = reverse_lazy('gen:gen_puntaje_add') #add
        context['url_form_edit'] = 'gen:gen_puntaje_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'pun_nombre': None,
                                  'pun_apellido': None,
                                  'pun_fecha' : None,
                                  'pun_email' : None,
                                  'pun_emailprofesor' : None,
                                  'pun_institucion': None,
                                  'pun_curso': None,
                                  'pun_materia': None,
                                  'pun_puntaje': None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.pun_id)
        return context


# Agregar
class Gen_PuntajeCreateView(CreateView):
    model = Gen_Puntaje
    form_class = Gen_PuntajeForm
    template_name = 'gen_puntaje/form.html'
    success_url = reverse_lazy('gen:gen_puntaje_list')

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
        kwargs = super(Gen_PuntajeCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
    # def get_initial(self):
    #     return {'emp_id': self.request.session.get('AIGN_EMP_ID')}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True

        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:
                form.save()
                messages.success(request, CRUD_MSG.CREATE)
                return HttpResponseRedirect(self.success_url)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errors = form.errors.setdefault("all_", ErrorList())
        errors.extend(extra_errors)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        return context


# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_PuntajeUpdateView(UpdateView):
    model = Gen_Puntaje
    form_class = Gen_PuntajeForm
    template_name = 'gen_puntaje/form.html'
    success_url = reverse_lazy('gen:gen_puntaje_list')

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
        kwargs = super(Gen_PuntajeUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        # for k in self.kwargs.keys():
        #     self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []

        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                form.save()
                messages.success(request, CRUD_MSG.SAVE)
                return HttpResponseRedirect(self.success_url)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                #Aqui instrucción para eliminado form.delete()
                self.get_object().delete()
                messages.success(request, CRUD_MSG.DELETE)
                return HttpResponseRedirect(self.success_url)
            except django.db.utils.InternalError as e:
                extra_errors.append(str(e))

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errors = form.errors.setdefault("all_", ErrorList())
        errors.extend(extra_errors)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        context['is_edit'] = 1
        return context
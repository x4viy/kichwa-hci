# Autor: Dre
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
from django.shortcuts import redirect
from apps.sis.forms import Sis_RolForm
from apps.sis.models import Sis_Rol
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
#
_e = EncryptDES()

# Listar
class Sis_RolListView(ListView):
    model = Sis_Rol
    template_name = 'sis_rol/list.html'

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Sis_Rol.objects.filter(rol_estado=1)
        return Sis_Rol.objects.all()

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(rol_usuario_actual)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('sis:sis_rol_add') #add
        context['url_form_add'] = reverse_lazy('sis:sis_rol_add') #add
        context['url_form_edit'] = 'sis:sis_rol_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'rol_nombre': None,
                                  'rol_tipo': None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.rol_id)
        return context


# Agregar
class Sis_RolCreateView(CreateView):
    model = Sis_Rol
    form_class = Sis_RolForm
    template_name = 'sis_rol/form.html'
    success_url = reverse_lazy('sis:sis_rol_list')

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_RolCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
    # def get_initial(self):
    #     nombre_usuario = self.request.session['AIGN_USUARIO']

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            print('')
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)
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
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        global rol_usuario_actual
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        return context


# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Sis_RolUpdateView(UpdateView):
    model = Sis_Rol
    form_class = Sis_RolForm
    template_name = 'sis_rol/form.html'
    success_url = reverse_lazy('sis:sis_rol_list')

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_RolUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        # for k in self.kwargs.keys():
        #     self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            print('')
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)
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
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        return context

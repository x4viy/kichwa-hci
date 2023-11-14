# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Vista para la opción informaciondetalle.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar

import django.db.models.query_utils
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.sis.models import *
from apps.sis.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
#
_e = EncryptDES()


# Listar
class Sis_InformaciondetalleListView(ListView):
    model = Sis_Informaciondetalle
    template_name = 'sis_informaciondetalle/list.html'

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Sis_Informaciondetalle.objects.filter(opc_estado=1)
        return Sis_Informaciondetalle.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('sis:sis_informaciondetalle_add') #add
        context['url_form_add'] = reverse_lazy('sis:sis_informaciondetalle_add') #add
        context['url_form_edit'] = 'sis:sis_informaciondetalle_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'inf_id':None,
                    'ind_nombre':None,
                    'ind_descripcion':None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.ind_id)
        return context


# Agregar
class Sis_InformaciondetalleCreateView(CreateView):
    model = Sis_Informaciondetalle
    form_class = Sis_InformaciondetalleForm
    template_name = 'sis_informaciondetalle/form.html'
    success_url = reverse_lazy('sis:sis_informaciondetalle_list')

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_InformaciondetalleCreateView, self).get_form_kwargs()
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
        print('ENTRE AL CREAR')
        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:
                print('exito DIOSITOO')
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
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        return context


# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Sis_InformaciondetalleUpdateView(UpdateView):
    model = Sis_Informaciondetalle
    form_class = Sis_InformaciondetalleForm
    template_name = 'sis_informaciondetalle/form.html'
    success_url = reverse_lazy('sis:sis_informaciondetalle_list')

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_InformaciondetalleUpdateView, self).get_form_kwargs()
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
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        return context

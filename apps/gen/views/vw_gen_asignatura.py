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
class Gen_AsignaturaListView(ListView):
    model = Gen_Asignatura
    template_name = 'gen_asignatura/list.html'

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Gen_Asignatura.objects.filter(cat_estado=1)
        return Gen_Asignatura.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_asignatura_add') #add
        context['url_form_add'] = reverse_lazy('gen:gen_asignatura_add') #add
        context['url_form_edit'] = 'gen:gen_asignatura_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'asi_nombre': None,
                                  'asi_descripcion': None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.asi_id)
        return context


# Agregar
class Gen_AsignaturaCreateView(CreateView):
    model = Gen_Asignatura
    form_class = Gen_AsignaturaForm
    template_name = 'gen_asignatura/form.html'
    success_url = reverse_lazy('gen:gen_asignatura_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_AsignaturaCreateView, self).get_form_kwargs()
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
class Gen_AsignaturaUpdateView(UpdateView):
    model = Gen_Asignatura
    form_class = Gen_AsignaturaForm
    template_name = 'gen_asignatura/form.html'
    success_url = reverse_lazy('gen:gen_asignatura_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_AsignaturaUpdateView, self).get_form_kwargs()
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
                print(self.get_object())
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

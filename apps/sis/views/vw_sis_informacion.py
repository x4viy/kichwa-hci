# Autor: Dre
# Fecha: 17/12/2022 010:00
# Descripción: Vista para la opción categorias.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar
import json
import django.db.models.query_utils
import pandas as pd
from django.shortcuts import redirect
import self as self
from django.db import transaction, connection
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.sis.forms import Sis_InformacionForm, get_SisInformacionDetsForm
from apps.sis.models import Sis_Informacion, Sis_Informaciondetalle
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG

#
_e = EncryptDES()


# Listar
class Sis_InformacionListView(ListView):
    model = Sis_Informacion
    template_name = 'sis_informacion/list.html'

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Sis_Informacion.objects.filter(inf_estado=1)
        return Sis_Informacion.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('sis:sis_informacion_add')  # add
        context['url_form_add'] = reverse_lazy('sis:sis_informacion_add')  # add
        context['url_form_edit'] = 'sis:sis_informacion_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'inf_nombre': None,
                                  'inf_descripcion': None}
        # # ecriptacion del id
        for r in context['object_list']:
            # r.inf_id = _e.encrypt(r.inf_id)
            r.inf_id = r.inf_id
        return context


# Agregar


class Sis_InformacionCreateView(CreateView):
    model = Sis_Informacion
    form_class = Sis_InformacionForm
    template_name = 'sis_informacion/form.html'
    success_url = reverse_lazy('sis:sis_informacion_list')


    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_InformacionCreateView, self).get_form_kwargs()
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
        r = {'a': 1}
        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_InformacionDetalle = pd.DataFrame(json.loads(request.POST['informaciondetalle_grid']))
                with transaction.atomic():
                    cabecera = form.save(commit=False)
                    cabecera.save()
                    for index, row in data_grid_InformacionDetalle.iterrows():
                        print(row.ind_nombre)
                        print(row[1])
                        # print(row.ind_descripcion)
                        infor = Sis_Informaciondetalle()
                        infor.inf_id = cabecera.pk
                        infor.inf_id = cabecera.inf_id
                        infor.ind_nombre = row.ind_nombre
                        infor.ind_descripcion = row[1]
                        infor.save()
                messages.success(request, CRUD_MSG.CREATE)
                return JsonResponse(r)
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
        ret = []
        ret.append(get_SisInformacionDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        return context


# Editar

# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Sis_InformacionUpdateView(UpdateView):
    model = Sis_Informacion
    form_class = Sis_InformacionForm
    template_name = 'sis_informacion/form.html'
    success_url = reverse_lazy('sis:sis_informacion_list')


    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_InformacionUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        for k in self.kwargs.keys():
            # self.kwargs[k] = _e.decrypt(self.kwargs[k])
            self.kwargs[k] = self.kwargs[k]
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}
        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_InformacionDetalle = pd.DataFrame(json.loads(request.POST['informaciondetalle_grid']))
                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    cabecera.save()
                    for index, row in data_grid_InformacionDetalle.iterrows():
                        infor = Sis_Informaciondetalle()
                        # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
                        if 'ind_id' in data_grid_InformacionDetalle:
                            if not pd.isna(row.ind_id):
                                infor.ind_id = row.ind_id
                                infor.inf_id = cabecera.pk
                                infor.ind_nombre = row.ind_nombre
                                infor.ind_descripcion = row.ind_descripcion
                                infor.ind_estado = 0 if row._action == 'E' else 1
                            # ERROR: Solo se puede modificar una respuesta (Solo se puede modificar la primera a falso.)

                            else:
                                infor.inf_id = cabecera.pk
                                infor.ind_nombre = row.ind_nombre
                                infor.ind_descripcion = row.ind_descripcion

                        else:
                            infor.inf_id = cabecera.pk
                            infor.ind_nombre = row.ind_nombre
                            infor.ind_descripcion = row.ind_descripcion
                        infor.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_InformacionDetalle = pd.DataFrame(json.loads(request.POST['informaciondetalle_grid']))
                with transaction.atomic():
                    # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                    # el pk desde el metodo dispach
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from sis.informaciondetalle
                              where inf_id = %s""",
                            [self.kwargs['pk']])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from sis.informacion
                              where inf_id = %s""",
                            [self.kwargs['pk']])
                    # Se elimina la cabecera
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        ret = []
        if 'pk' in context:
            opc_id = _e.decrypt(context['pk'])
            print(opc_id)

        else:
            inf_id = context['object'].inf_id
            # tem_nombre = context['object'].tem_nombre
            # tem_descripcion = context['object'].tem_descripcion
            # mul_archivo = context['object'].mul_archivo
            # print('TEMID ', tem_id)
            # print('TEMNOMBRE ', tem_nombre)
            # print('TEMDESC ', tem_descripcion)
            # print('MULARCHIVO ', mul_archivo)
        ret.append(get_SisInformacionDetsForm(inf_id).to_JSON())
        context['grids_detalles'] = ret
        return context

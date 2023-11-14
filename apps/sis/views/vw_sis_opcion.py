# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Vista para la opción opcion.
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
from apps.sis.models import *
from apps.sis.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from django.shortcuts import redirect
from vars.msg import CRUD_MSG
#
_e = EncryptDES()

# Autor: Bryan Amaya
# Listar
class Sis_OpcionListView(ListView):
    model = Sis_Opcion
    template_name = 'sis_opcion/list.html'

    # Autor: Bryan Amaya
    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Sis_Opcion.objects.filter(opc_estado=1)
        return Sis_Opcion.objects.all()

    # Autor: Bryan Amaya
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('sis:sis_opcion_add') #add
        context['url_form_add'] = reverse_lazy('sis:sis_opcion_add') #add
        context['url_form_edit'] = 'sis:sis_opcion_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'opc_idpadre':None,
                    'opc_nombre':None,
                    'opc_codigov':None,
                    'opc_descripcion':None,
                    'opc_url':None,
                    'opc_icono':None,
                    'opc_tipo':None,
                    'opc_orden':None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.opc_id = _e.encrypt(r.opc_id)
        return context

# Autor: Bryan Amaya
# Agregar
class Sis_OpcionCreateView(CreateView):
    model = Sis_Opcion
    form_class = Sis_OpcionForm
    template_name = 'sis_opcion/form.html'
    success_url = reverse_lazy('sis:sis_opcion_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Autor: Bryan Amaya
    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_OpcionCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
    # def get_initial(self):
    #     return {'emp_id': self.request.session.get('AIGN_EMP_ID')}
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
                data_grid_OpcionRol = pd.DataFrame(json.loads(request.POST['opcionrol_grid']))
                print('respopcrol0 :', data_grid_OpcionRol)
                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    cabecera.save()
                    for index, row in data_grid_OpcionRol.iterrows():

                        respopcrol = Sis_OpcionRol()
                        print('cabeceraa :', cabecera)
                        print('respopcrol1 :', respopcrol)
                        respopcrol.opc_id = cabecera.pk
                        print('respopcrol2 :', respopcrol.opc_id)              
                        print('respopcrol3 :', respopcrol.rol_id)
                        respopcrol.rol_id = row.rol_id
                        respopcrol.oro_esactivo = row.oro_esactivo
                        respopcrol.oro_estado = 1
                        respopcrol.save()
                messages.success(request, CRUD_MSG.CREATE)
                return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errors = form._errors.setdefault("__all__", ErrorList())
        errors.extend(extra_errors)
        return JsonResponse(dict(form._errors.items()))

    # Autor: Bryan Amaya
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        ret = []
        ret.append(get_sisOpcionRolDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        return context

# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Sis_OpcionUpdateView(UpdateView):
    model = Sis_Opcion
    form_class = Sis_OpcionForm
    template_name = 'sis_opcion/form.html'
    success_url = reverse_lazy('sis:sis_opcion_list')

    # Autor: Bryan Amaya
    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_OpcionUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    # Autor: Bryan Amaya
    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        for k in self.kwargs.keys():
            self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}


        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_OpcionRol = pd.DataFrame(json.loads(request.POST['opcionrol_grid']))
                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    cabecera.save()
                    for index, row in data_grid_OpcionRol.iterrows():
                        print('index :', index)
                        print('row :', row)
                        respopcrol = Sis_OpcionRol()
                        # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
                        if 'oro_id' in data_grid_OpcionRol:
                            if not pd.isna(row.oro_id):
                                print('mul2')
                                print('cabbbb ', cabecera.pk)
                                respopcrol.oro_id = row.oro_id
                                respopcrol.opc_id = cabecera.pk
                                respopcrol.rol_id = row.rol_id
                                respopcrol.oro_esactivo = row.oro_esactivo
                                respopcrol.oro_estado = 1
                                # ERROR: Solo se puede modificar una respuesta (Solo se puede modificar la primera a falso.)
                                respopcrol.oro_estado = 0 if row._action == 'E' else 1
                            else:
                                print('mul3')
                                respopcrol.opc_id = cabecera.pk
                                respopcrol.rol_id = row.rol_id
                                respopcrol.oro_esactivo = row.oro_esactivo
                                # respopcrol.oro_estado = 1
                        else:
                            print('mul4')
                            respopcrol.opc_id = cabecera.pk
                            respopcrol.rol_id = row.rol_id
                            respopcrol.oro_esactivo = row.oro_esactivo
                            # respopcrol.oro_estado = 1
                        respopcrol.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_OpcionRol = pd.DataFrame(json.loads(request.POST['opcionrol_grid']))
                with transaction.atomic():
                    # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                    # el pk desde el metodo dispach
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from sis.opcion_rol
                              where opc_id = %s""",
                            [self.kwargs['pk']])
                    # Se elimina la cabecera
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

    # Autor: Bryan Amaya
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        context['is_edit'] = 1
        ret = []
        if 'pk' in context:
            opc_id = _e.decrypt(context['pk'])
            print(opc_id)

        else:
            opc_id = context['object'].opc_id
            print(opc_id)
        ret.append(get_sisOpcionRolDetsForm(opc_id).to_JSON())
        context['grids_detalles'] = ret
        return context

# Tema
# Autor: Bryan Amaya
# Fecha: 07/05/2023 17:00
# Descripción: Vista para la opción cabecera tema, detalle actividad.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar

import os
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
from django.shortcuts import redirect
#
_e = EncryptDES()

Contador = 0
# Autor: Bryan Amaya
# Listar
class Gen_TemaListView(ListView):
    model = Gen_Tema
    template_name = 'gen_tema/list.html'
    ordering = ['tem_id']  # Agrega esta línea para ordenar por tem_id
    # Autor: Bryan Amaya

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        usuario_actual = self.request.session['AIGN_USERID']
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
            return Gen_Tema.objects.all()
            # return 1
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_Tema.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_Tema.objects.none()

    # Autor: Bryan Amaya
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_tema_add') #add
        context['url_form_add'] = reverse_lazy('gen:gen_tema_add') #add
        context['url_form_edit'] = 'gen:gen_tema_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {# 'tem_id':None,
                    # 'usu_id':None,
                    'asi':None,
                    'tem_nombre':None,
                    'tem_descripcion':None
                    }
        # # ecriptacion del id
        for r in context['object_list']:
            # r.tem_id = _e.encrypt(r.tem_id)
            r.tem_id = r.tem_id
        return context

# Autor: Bryan Amaya
# Agregar
class Gen_TemaCreateView(CreateView):
    model = Gen_Tema
    form_class = Gen_TemaForm
    template_name = 'gen_tema/form.html'
    success_url = reverse_lazy('gen:gen_tema_list')

    def get(self, request, *args, **kwargs):
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
        kwargs = super(Gen_TemaCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # Iniciallizar el formulario
    def get_initial(self):
        mul_id = self.request.session.get('AIGN_MUL_ID')
        multimedia = Gen_Multimedia.objects.filter(mul_id = mul_id)
        return {'mul_id': self.request.session.get('AIGN_MUL_ID')}
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

                data_grid_TemaActividad = pd.DataFrame(json.loads(request.POST['temaactividad_grid']))
                # print('tab_temaactividad0 :', data_grid_TemaActividad)
                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    global Contador
                    # print('Contador ', Contador)
                    Contador = Contador + 1
                    # print('Contador ', Contador)
                    if not data_grid_TemaActividad.empty:
                        for index, row in data_grid_TemaActividad.iterrows():
                            formcomp = Gen_TemaForm(request.POST, request.FILES)
                            if formcomp.is_valid():
                                # Imprimir datos del formulario en consola
                                # print(formcomp.cleaned_data['usu_id'])
                                # print(formcomp.cleaned_data['asi'])
                                # print(formcomp.cleaned_data['mul_id'])
                                # print(formcomp.cleaned_data['tem_nombre'])
                                # print(formcomp.cleaned_data['tem_descripcion'])
                                if formcomp.cleaned_data.get('mul_archivo', None) and Contador == 1:
                                    # print('XD', formcomp.cleaned_data['mul_archivo'])
                                    tab_multimedia = Gen_Multimedia()
                                    archivo = formcomp.cleaned_data['mul_archivo']
                                    ext = os.path.splitext(archivo.name)
                                    # print('FORMATO ', ext[1])
                                    tab_multimedia.tem_id = cabecera.pk
                                    tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                                    tab_multimedia.mul_tipo = 'Imagen'
                                    tab_multimedia.mul_formato= ext[1]
                                    tab_multimedia.save()

                            tab_temaactividad = Gen_TemaActividad()
                            # tab_multimedia.mul_archivo =
                            # print('cabeceraa :', cabecera)
                            # print('tab_temaactividad1 :', tab_temaactividad)
                            # for attribute, value in row.items():
                                # print(f'{attribute}: {value}')
                            # tab_temaactividad.tac_id = row.tac_id
                            tab_temaactividad.act_id = row.act_id
                            # print('tab_temaactividad2 :', tab_temaactividad.act_id)
                            # print('tab_temaactividad3 :', tab_temaactividad.tem_id)
                            tab_temaactividad.tem_id = cabecera.pk
                            # tab_temaactividad.act_nombre = row.act_nombre
                            # tab_temaactividad.act_descripcion = row.act_descripcion
                            tab_temaactividad.tac_estado = 1
                            usuario_actual = self.request.session['AIGN_USERID']
                            tab_temaactividad.usuario_actual = usuario_actual
                            tab_temaactividad.save()
                            Contador = Contador - 1
                    else:
                        formcomp = Gen_TemaForm(request.POST, request.FILES)
                        if formcomp.is_valid():
                            if formcomp.cleaned_data.get('mul_archivo', None):
                                # print('XD', formcomp.cleaned_data['mul_archivo'])
                                tab_multimedia = Gen_Multimedia()
                                archivo = formcomp.cleaned_data['mul_archivo']
                                ext = os.path.splitext(archivo.name)
                                # print('FORMATO ', ext[1])
                                tab_multimedia.tem_id = cabecera.pk
                                tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                                tab_multimedia.mul_tipo = 'Imagen'
                                tab_multimedia.mul_formato = ext[1]
                                tab_multimedia.save()

                    # print('AHORA SI FINALICE EL CREAR')
                messages.success(request, CRUD_MSG.CREATE)
                return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))
        # print('FINALICE CREAR')
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
        ret.append(get_genTemaActividadDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        return context

# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_TemaUpdateView(UpdateView):
    model = Gen_Tema
    form_class = Gen_TemaForm
    template_name = 'gen_tema/form.html'
    success_url = reverse_lazy('gen:gen_tema_list')

    def get(self, request, *args, **kwargs):
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
        kwargs = super(Gen_TemaUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    # Autor: Bryan Amaya
    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        for k in self.kwargs.keys():
            # self.kwargs[k] = _e.decrypt(self.kwargs[k])
            self.kwargs[k] = self.kwargs[k]
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        multimedia = Gen_Multimedia.objects.filter(tem_id=self.kwargs['pk']).only('mul_id')
        archivo = Gen_Multimedia.objects.filter(tem_id=self.kwargs['pk']).only('mul_archivo')
        if multimedia.exists():
            return {'mul_id': multimedia[0].mul_id, 'mul_archivo': archivo[0].mul_archivo}
            # return {'mul_id': multimedia[0].mul_id, 'mul_archivo_existente': archivo[0].mul_archivo}
        return {}

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
                data_grid_TemaActividad = pd.DataFrame(json.loads(request.POST['temaactividad_grid']))
                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    formcomp = Gen_TemaForm(request.POST, request.FILES)
                    if formcomp.is_valid():
                        # Imprimir datos del formulario en consola
                        # print(formcomp.cleaned_data['usu_id'])
                        # print(formcomp.cleaned_data['asi'])
                        # print(formcomp.cleaned_data['tem_nombre'])
                        # print(formcomp.cleaned_data['tem_descripcion'])
                        # Si existe un mul id, es decir hay una imagen cargada
                        if formcomp.cleaned_data.get('mul_id', None):
                            # Si existe un archivo nuevo, es decir se quiere modificar la imagen
                            if formcomp.cleaned_data.get('mul_archivo', None):
                                # print('XDXDXDXD', formcomp.cleaned_data['mul_id'])
                                # print('Xmmmmmmmmmmmmmmmmmmmmmm', formcomp.cleaned_data['mul_archivo'])
                                tab_multimedia = Gen_Multimedia.objects.get(mul_id=formcomp.cleaned_data['mul_id'])
                                # tab_multimedia.mul_archivo.delete()
                                # print('name ', tab_multimedia.mul_archivo.name)
                                # print(tab_multimedia.mul_archivo.path)
                                file_path = os.path.join(settings.MEDIA_ROOT, tab_multimedia.mul_archivo.name[len(settings.MEDIA_URL):])
                                # print('avemaria ', file_path)
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                # print('xcdddddddddddddddddddd')
                                archivo = formcomp.cleaned_data['mul_archivo']
                                ext = os.path.splitext(archivo.name)
                                # print('FORMATO ', ext[1])
                                # tab_multimedia.tem_id = cabecera.pk
                                tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                                tab_multimedia.mul_tipo = 'Imagen'
                                tab_multimedia.mul_formato = ext[1]
                                tab_multimedia.save()
                            # Si no existe un archivo nuevo, es decir se buscan modificar cosas que no tienen que ver con la imagen
                            else:
                                tab_multimedia = Gen_Multimedia.objects.get(mul_id=formcomp.cleaned_data['mul_id'])
                                tab_multimedia.mul_archivo = tab_multimedia.mul_archivo
                                tab_multimedia.mul_tipo = tab_multimedia.mul_tipo
                                tab_multimedia.mul_formato = tab_multimedia.mul_formato
                                tab_multimedia.save()
                        # Si no existe un archivo previo y se quiere agregar uno nuevo.
                        elif formcomp.cleaned_data.get('mul_archivo', None):
                            # print('XDXDXDXD2', formcomp.cleaned_data['mul_id'])
                            tab_multimedia = Gen_Multimedia()
                            archivo = formcomp.cleaned_data['mul_archivo']
                            ext = os.path.splitext(archivo.name)
                            # print('FORMATO2 ', ext[1])
                            tab_multimedia.tem_id = cabecera.pk
                            tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                            tab_multimedia.mul_tipo = 'Imagen'
                            tab_multimedia.mul_formato = ext[1]
                            tab_multimedia.save()
                    # print('CABECERAAAAAAAAAAAAA ', cabecera.pk)
                    for index, row in data_grid_TemaActividad.iterrows():
                        tab_temaactividad = Gen_TemaActividad()
                        # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
                        if 'tac_id' in data_grid_TemaActividad:
                            # Si es que hay datos en la grilla
                            if not pd.isna(row.tac_id):
                                print('MULTIMPORTANTE1.2 ', row.tac_id)
                                tab_temaactividad.tac_id = row.tac_id
                                tab_temaactividad.act_id = row.act_id
                                tab_temaactividad.tem_id = cabecera.pk
                                # tab_temaactividad.act_nombre = row.act_nombre
                                # tab_temaactividad.act_descripcion = row.act_descripcion
                                tab_temaactividad.tac_estado = 0 if row._action == 'E' else 1
                            # Si no hay datos en la grilla
                            else:
                                print('MULTIMPORTANTE1.3 ', row.act_id)
                                tab_temaactividad.tem_id = cabecera.pk
                                tab_temaactividad.act_id = row.act_id
                                # tab_temaactividad.act_nombre = row.act_nombre
                                # tab_temaactividad.act_descripcion = row.act_descripcion
                        else:
                            print('MULTIMPORTANTE1.4 ')
                            tab_temaactividad.tem_id = cabecera.pk
                            tab_temaactividad.act_id = row.act_id
                            # tab_temaactividad.act_nombre = row.act_nombre
                            # tab_temaactividad.act_descripcion = row.act_descripcion
                        usuario_actual = self.request.session['AIGN_USERID']
                        tab_temaactividad.usuario_actual = usuario_actual
                        tab_temaactividad.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_TemaActividad = pd.DataFrame(json.loads(request.POST['temaactividad_grid']))
                with transaction.atomic():
                    # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                    # el pk desde el metodo dispach
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """SELECT mul_archivo FROM gen.multimedia
                               WHERE tem_id = %s""",
                            [self.kwargs['pk']])
                        result = cursor.fetchone()
                        if result:
                            imagen_url = result[0]
                        else:
                            imagen_url = None
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from gen.tema_actividad
                              where tem_id = %s""",
                            [self.kwargs['pk']])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from gen.multimedia
                              where tem_id = %s""",
                            [self.kwargs['pk']])
                    # Se elimina la cabecera
                    self.get_object().delete()
                    if imagen_url:
                        print('existe_imagen')
                        print(imagen_url)
                        file_path = os.path.join(settings.MEDIA_ROOT, imagen_url[len(settings.MEDIA_URL):])
                        print(file_path)
                        if os.path.exists(file_path):
                            os.remove(file_path)
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
        ret = []
        if 'pk' in context:
            opc_id = _e.decrypt(context['pk'])
            print(opc_id)

        else:
            tem_id = context['object'].tem_id
            tem_nombre = context['object'].tem_nombre
            tem_descripcion = context['object'].tem_descripcion
            # mul_archivo = context['object'].mul_archivo
            print('TEMID ', tem_id)
            print('TEMNOMBRE ', tem_nombre)
            print('TEMDESC ', tem_descripcion)
            # print('MULARCHIVO ', mul_archivo)
        ret.append(get_genTemaActividadDetsForm(tem_id).to_JSON())
        context['grids_detalles'] = ret
        return context

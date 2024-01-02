# # Autor: Bryan Amaya
# # Fecha: 06/05/2023 22:55
# # Descripción: Vista para la opción juego.
# #              En esta opción permite:
# #              listar, agregar, modificar, eliminar
#
# import django.db.models.query_utils
# from django.forms.utils import ErrorList
# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.urls import reverse_lazy
# from django.views.generic import ListView, UpdateView, CreateView
# from apps.gen.models import *
# from apps.gen.forms import *
# from vars.js import datatable_opts
# from django.contrib import messages
# from core.encryption_util import *
# from utils import utils
# from vars.msg import CRUD_MSG
# #
# _e = EncryptDES()
#
#
# # Listar
# class Gen_JuegoListView(ListView):
#     model = Gen_Juego
#     template_name = 'gen_juego/list.html'
#
#     def get_queryset(self):
#         emp_filter = self.request.session.get('AIGN_EMP_ID')
#         if emp_filter:
#             return Gen_Juego.objects.filter(jue_estado=1)
#         return Gen_Juego.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
#         context['url_form'] = reverse_lazy('gen:gen_juego_add') #add
#         context['url_form_add'] = reverse_lazy('gen:gen_juego_add') #add
#         context['url_form_edit'] = 'gen:gen_juego_edit' #edit
#         context['datatable_id'] = 'datatable1_id'
#         context['datatable_opts'] = datatable_opts
#         # Agregar boton 'Agregar' lista
#         context['show_fields'] = {'act': None,
#                                   'jue_nombre': None,
#                                   'jue_descripcion': None,
#                                   'jue_tipo': None,
#                                   'jue_enunciado': None,
#                                   'jue_puntaje': None}
#         # # ecriptacion del id
#         for r in context['object_list']:
#             r.jue_id = _e.encrypt(r.jue_id)
#         return context
#
#
# # Agregar
# class Gen_JuegoCreateView(CreateView):
#     model = Gen_Juego
#     form_class = Gen_JuegoForm
#     template_name = 'gen_juego/form.html'
#     success_url = reverse_lazy('gen:gen_juego_list')
#
#     # Asigna al kwargs la variable de session desde el formulario
#     def get_form_kwargs(self):
#         kwargs = super(Gen_JuegoCreateView, self).get_form_kwargs()
#         # #Roles
#         # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
#         # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
#         return kwargs
#
#     # # Iniciallizar el formulario
#     # def get_initial(self):
#     #     return {'emp_id': self.request.session.get('AIGN_EMP_ID')}
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         extra_errors = []
#         request.POST._mutable = True
#
#         # Crear el registro
#         if 'CREATE' in request.POST and form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, CRUD_MSG.CREATE)
#                 return HttpResponseRedirect(self.success_url)
#             except django.db.models.query_utils.InvalidQuery as e:
#                 extra_errors.append(str(e))
#
#         self.object = None
#         context = self.get_context_data(**kwargs)
#         context['form'] = form
#         errors = form._errors.setdefault("__all__", ErrorList())
#         errors.extend(extra_errors)
#         return render(request, self.template_name, context)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = self.model._meta.verbose_name
#         context['url_list'] = self.success_url
#         return context
#
#
# # Editar
# # Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
# class Gen_JuegoUpdateView(UpdateView):
#     model = Gen_Juego
#     form_class = Gen_JuegoForm
#     template_name = 'gen_juego/form.html'
#     success_url = reverse_lazy('gen:gen_juego_list')
#
#     # Asigna al kwargs la variable de session desde el formulario
#     def get_form_kwargs(self):
#         kwargs = super(Gen_JuegoUpdateView, self).get_form_kwargs()
#         # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
#         # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
#         return kwargs
#
#     def dispatch(self, request, *args, **kwargs):
#         # Desencriptando el pk
#         for k in self.kwargs.keys():
#             self.kwargs[k] = _e.decrypt(self.kwargs[k])
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         extra_errors = []
#
#         # Editar
#         if 'SAVE' in request.POST and form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, CRUD_MSG.SAVE)
#                 return HttpResponseRedirect(self.success_url)
#             except django.db.models.query_utils.InvalidQuery as e:
#                 extra_errors.append(str(e))
#
#         # Eliminar
#         if 'DELETE' in request.POST and form.is_valid():
#             try:
#                 #Aqui instrucción para eliminado form.delete()
#                 self.get_object().delete()
#                 messages.success(request, CRUD_MSG.DELETE)
#                 return HttpResponseRedirect(self.success_url)
#             except django.db.utils.InternalError as e:
#                 extra_errors.append(str(e))
#
#         self.object = None
#         context = self.get_context_data(**kwargs)
#         context['form'] = form
#         errors = form._errors.setdefault("__all__", ErrorList())
#         errors.extend(extra_errors)
#         return render(request, self.template_name, context)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = self.model._meta.verbose_name
#         context['url_list'] = self.success_url
#         return context


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
class Gen_JuegoListView(ListView):
    model = Gen_Juego
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
            return Gen_Juego.objects.all()
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_Juego.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_Juego.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_juego_add')  # add
        context['url_form_add'] = reverse_lazy('gen:gen_juego_add')  # add
        context['url_form_edit'] = 'gen:gen_juego_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'tac': None,
                                  'tip': None,
                                  'jue_nombre': None,
                                  'jue_descripcion': None,
                                  'jue_enunciado': None,
                                  'jue_puntaje': None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.jue_id = _e.encrypt(r.jue_id)
        return context


# Autor: Bryan Amaya
# Agregar
# Agregar
class Gen_JuegoCreateView(CreateView):
    model = Gen_Juego
    form_class = Gen_JuegoForm
    template_name = 'gen_juego/form.html'
    success_url = reverse_lazy('gen:gen_juego_list')

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
        kwargs = super(Gen_JuegoCreateView, self).get_form_kwargs()
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
                print("adentro   ", request.POST)
                data_grid_Respuesta = pd.DataFrame(json.loads(request.POST['respuesta_grid']))
                print('tab_respuesta0 :', data_grid_Respuesta)
                print('tab_respuesta1 :', json.loads(request.POST['respuesta_grid']))
                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    true_count = sum(1 for index, row in data_grid_Respuesta.iterrows() if row.res_escorrecta)
                    # print("Cantidad de respuestas correctas:", true_count)
                    if true_count != 1:
                        extra_errors = ErrorList()

                        # Agrega tus errores personalizados a extra_errors
                        extra_errors.append("Solo puede existir una respuesta correcta.")

                        # Agrega los errores a form._errors
                        errors = form._errors.setdefault("__all__", ErrorList())
                        errors.extend(extra_errors)

                        # Convierte los errores a un diccionario
                        errors_dict = dict(form.errors.items())

                        # Agrega tus errores personalizados al diccionario
                        errors_dict['custom_errors'] = extra_errors
                        return JsonResponse(errors_dict)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    for index, row in data_grid_Respuesta.iterrows():
                        tab_respuesta = Gen_Respuesta()
                        tab_multimedia = Gen_Multimedia()
                        # cabecera.pk es el id del registro de la base de datos
                        tab_respuesta.jue_id = cabecera.pk
                        # Como nuestro modelo actividad ya tiene una relación de tem
                        # nosotros podemos acceder a cualquier field de tem
                        # basta con agregarle guion bajo, ejemplo tem_id, tem_nombre, etc
                        tab_respuesta.res_respuesta = row.res_respuesta
                        tab_respuesta.res_escorrecta = row.res_escorrecta
                        tab_respuesta.save()
                        tema_actividad = Gen_TemaActividad.objects.get(tac_id=cabecera.tac_id)
                        # tab_multimedia.mul_id = row.mul_id
                        if 'mul_archivo' in row:
                            if str(row.mul_archivo).lower() != 'nan':
                                tab_multimedia.tem_id = tema_actividad.tem_id
                                tab_multimedia.act_id = tema_actividad.act_id
                                tab_multimedia.res_id = tab_respuesta.res_id
                                tab_multimedia.jue_id = cabecera.pk
                                tab_multimedia.mul_archivo = row.mul_archivo
                                tab_multimedia.mul_tipo = row.mul_tipo
                                tab_multimedia.mul_formato = row.mul_formato
                                # print('PRINT MIXTOOOOO' , row.mul_archivo)
                                tab_multimedia.save()
                print("r ", r)
                messages.success(request, CRUD_MSG.CREATE)
                print("request", request)
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
        ret.append(get_genRespuestaDetsForm(None).to_JSON())
        # ret.append(get_genMultimediaDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        # print('8')
        return context


# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_JuegoUpdateView(UpdateView):
    model = Gen_Juego
    form_class = Gen_JuegoForm
    template_name = 'gen_juego/form.html'
    success_url = reverse_lazy('gen:gen_juego_list')

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
        kwargs = super(Gen_JuegoUpdateView, self).get_form_kwargs()
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

        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_Respuesta = pd.DataFrame(json.loads(request.POST['respuesta_grid']))
                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    true_count = sum(1 for index, row in data_grid_Respuesta.iterrows() if row.res_escorrecta)
                    # print("Cantidad de respuestas correctas:", true_count)
                    if true_count != 1:
                        raise django.core.exceptions.ValidationError("Debe haber una y solo una respuesta correcta.")
                        # print('pipipi')
                    # print('CABECERAAAAAAAAAAAAA ', cabecera.pk)
                    for index, row in data_grid_Respuesta.iterrows():
                        tab_respuesta = Gen_Respuesta()
                        # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
                        if 'res_id' in data_grid_Respuesta:
                            # Si se edita, es decir si existe un valor
                            if not pd.isna(row.res_id):
                                print('MULTIMPORTANTE1.2 ', row.res_id, row.res_respuesta,
                                      row.res_escorrecta)
                                tab_respuesta.res_id = row.res_id
                                tab_respuesta.jue_id = cabecera.pk
                                tab_respuesta.res_respuesta = row.res_respuesta
                                tab_respuesta.res_escorrecta = row.res_escorrecta
                                tab_respuesta.res_estado = 0 if row._action == 'E' else 1
                                # EN CASO DE ELIMINAR UN REGISTRO DE LA GRILLA AL EDITAR
                                if tab_respuesta.res_estado == 0:
                                    tab_multimedia = Gen_Multimedia()
                                    with transaction.atomic():
                                        # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                                        # el pk desde el metodo dispach
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                """SELECT mul_archivo FROM gen.multimedia
                                                   WHERE jue_id = %s AND res_id = %s""",
                                                [self.kwargs['pk'], tab_respuesta.res_id])
                                            result = cursor.fetchall()
                                            if result:
                                                imagen_url = result[0]
                                                # print(imagen_url)
                                            else:
                                                imagen_url = None

                                        # print(self.kwargs['pk'])
                                        # print(self.get_object())
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                """delete from gen.multimedia
                                                  where jue_id = %s AND res_id = %s""",
                                                [self.kwargs['pk'], tab_respuesta.res_id])
                                        # print(self.kwargs['pk'])
                                        # with connection.cursor() as cursor:
                                        #     cursor.execute(
                                        #         """delete from gen.respuesta
                                        #           where jue_id = %s""",
                                        #         [self.kwargs['pk']])
                                        # print(self.kwargs['pk'])
                                        # print(self.get_object())
                                        if imagen_url:
                                            # print('existe_imagen')
                                            for row in result:
                                                # print(row[0])
                                                imagen_url = row[0]
                                                file_path = os.path.join(settings.MEDIA_ROOT,
                                                                         imagen_url[len(settings.MEDIA_URL):])
                                                # print('yeyyyy ', file_path)
                                                if os.path.exists(file_path):
                                                    os.remove(file_path)

                            else:
                                print('MULTIMPORTANTE1.3 ', row.res_id, row.res_respuesta,
                                      row.res_escorrecta)
                                tab_respuesta.jue_id = cabecera.pk
                                tab_respuesta.res_respuesta = row.res_respuesta
                                tab_respuesta.res_escorrecta = row.res_escorrecta
                                tab_respuesta.save()
                                if not pd.isna(row.mul_archivo):
                                    tab_multimedia = Gen_Multimedia()
                                    tema_actividad = Gen_TemaActividad.objects.get(tac_id=cabecera.tac_id)
                                    tab_multimedia.tem_id = tema_actividad.tem_id
                                    tab_multimedia.act_id = tema_actividad.act_id
                                    tab_multimedia.res_id = tab_respuesta.res_id
                                    tab_multimedia.jue_id = cabecera.pk
                                    tab_multimedia.mul_archivo = row.mul_archivo
                                    tab_multimedia.mul_tipo = row.mul_tipo
                                    tab_multimedia.mul_formato = row.mul_formato
                                    # print('arch ', row.mul_archivo)
                                    # print('tip ', row.mul_tipo)
                                    # print('for ', row.mul_formato)
                                    tab_multimedia.save()
                        else:
                            print('MULTIMPORTANTE1.4 ', row.res_respuesta,
                                  row.res_escorrecta)
                            tab_respuesta.jue_id = cabecera.pk
                            tab_respuesta.res_respuesta = row.res_respuesta
                            tab_respuesta.res_escorrecta = row.res_escorrecta
                            tab_respuesta.save()
                            if not pd.isna(row.mul_archivo):
                                tab_multimedia = Gen_Multimedia()
                                tema_actividad = Gen_TemaActividad.objects.get(tac_id=cabecera.tac_id)
                                tab_multimedia.tem_id = tema_actividad.tem_id
                                tab_multimedia.act_id = tema_actividad.act_id
                                tab_multimedia.res_id = tab_respuesta.res_id
                                tab_multimedia.jue_id = cabecera.pk
                                tab_multimedia.mul_archivo = row.mul_archivo
                                tab_multimedia.mul_tipo = row.mul_tipo
                                tab_multimedia.mul_formato = row.mul_formato
                                tab_multimedia.save()
                        tab_respuesta.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                data_grid_Respuesta = pd.DataFrame(json.loads(request.POST['respuesta_grid']))
                with transaction.atomic():
                    # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                    # el pk desde el metodo dispach
                    # with connection.cursor() as cursor:
                    #     cursor.execute(
                    #         """delete from gen.respuesta
                    #           where jue_id = %s""",
                    #         [self.kwargs['pk']])
                    # # Se elimina la cabecera
                    # self.get_object().delete()
                    with transaction.atomic():
                        # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                        # el pk desde el metodo dispach
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """SELECT mul_archivo FROM gen.multimedia
                                   WHERE jue_id = %s""",
                                [self.kwargs['pk']])
                            result = cursor.fetchall()
                            if result:
                                imagen_url = result[0]
                            else:
                                imagen_url = None

                        # print(self.kwargs['pk'])
                        # print(self.get_object())
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """delete from gen.multimedia
                                  where jue_id = %s""",
                                [self.kwargs['pk']])
                        # print(self.kwargs['pk'])
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """delete from gen.respuesta
                                  where jue_id = %s""",
                                [self.kwargs['pk']])
                        # print(self.kwargs['pk'])
                        # print(self.get_object())
                        # with connection.cursor() as cursor:
                        #     cursor.execute(
                        #         """delete from gen.actividad
                        #           where act_id = %s""",
                        #         [self.kwargs['pk']])
                        # Se elimina la cabecera
                        # print(self.kwargs['pk'])
                        # print(self.get_object())
                        # print('que paso?')
                        # print(self.get_object())
                        # print('huh?')
                        self.get_object().delete()
                        if imagen_url:
                            # print('existe_imagen')
                            for row in result:
                                print(row[0])
                                imagen_url = row[0]
                                file_path = os.path.join(settings.MEDIA_ROOT, imagen_url[len(settings.MEDIA_URL):])
                                # print('yeyyyy ', file_path)
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
            jue_id = _e.decrypt(context['pk'])
        else:
            jue_id = context['object'].jue_id
        ret.append(get_genRespuestaDetsForm(jue_id).to_JSON())
        # ret.append(get_genMultimediaDetsForm(jue_id).to_JSON())
        context['grids_detalles'] = ret
        # print('15')
        return context

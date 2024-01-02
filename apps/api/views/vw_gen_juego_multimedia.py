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
class Gen_CartaListView(ListView):
    model = Gen_Carta
    template_name = 'gen_carta/list.html'

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
            return Gen_Carta.objects.all()
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_Carta.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_Carta.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('multimedia_game:gen_carta_add')  # add
        context['url_form_add'] = reverse_lazy('multimedia_game:gen_carta_add')  # add
        context['url_form_edit'] = 'multimedia_game:gen_carta_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {
            'cart_descripcion': None,
        }
        # # ecriptacion del id
        for r in context['object_list']:

            relacion_cartas_multimedia = Gen_CartaMultimedia.objects.filter(camu_cart_id=r.cart_id)
            r.cart_id = _e.encrypt(r.cart_id)
            r.alt = r.cart_descripcion

            for carta_multimedia in relacion_cartas_multimedia:
                identificador_archivo = carta_multimedia.camu_muar_id_id
                archivos_multimedia = Gen_MultimediaFile.objects.filter(muar_id=identificador_archivo,
                                                                        muar_tipo='image')
                for archivo_multimedia in archivos_multimedia:
                    ruta_archivo = archivo_multimedia.muar_ruta
                    r.ruta_archivo = ruta_archivo

        return context


# Autor: Bryan Amaya
# Agregar
class Gen_CartaCreateView(CreateView):
    model = Gen_Carta
    form_class = Gen_CartaForm
    template_name = 'gen_carta/create-card.html'
    success_url = reverse_lazy('multimedia_game:gen_carta_list')

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
        kwargs = super(Gen_CartaCreateView, self).get_form_kwargs()
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
                archivo_imagen = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))
                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    print('ultimo ingresado',cabecera.cart_id)
                    for index, row in archivo_imagen.iterrows():
                        tab_imagen = Gen_MultimediaFile()
                        if 'muar_ruta' in row:
                            if str(row.muar_ruta).lower() != 'nan':
                                tab_imagen.muar_ruta = row.muar_ruta
                                tab_imagen.muar_tipo = row.muar_tipo
                                tab_imagen.muar_formato = row.muar_formato
                                tab_imagen.save()
                                print('ultimo ingresado archivo', tab_imagen.muar_id)

                                relacion_carta_multimedia = Gen_CartaMultimedia()
                                relacion_carta_multimedia.camu_muar_id_id = tab_imagen.muar_id
                                relacion_carta_multimedia.camu_cart_id_id = cabecera.cart_id
                                relacion_carta_multimedia.save()

                messages.success(request, CRUD_MSG.CREATE)
                print("request", request)
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
        ret = []
        ret.append(get_genMultimediaFileDetsForm(None).to_JSON())
        print('ret  ', get_genMultimediaFileDetsForm(None).to_JSON())
        # ret.append(get_genMultimediaDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        # print('8')
        return context


# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_CartaUpdateView(UpdateView):
    model = Gen_Carta
    form_class = Gen_CartaForm
    template_name = 'gen_carta/create-card.html'
    success_url = reverse_lazy('multimedia_game:gen_carta_list')

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
        kwargs = super(Gen_CartaUpdateView, self).get_form_kwargs()
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

        print("adentro   ", request.POST['multimedia_file_grid'])
        print("json   ", pd.DataFrame(json.loads(request.POST['multimedia_file_grid'])))

        data_grid_multimedia = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))

        # # Editar
        # if 'SAVE' in request.POST and form.is_valid():
        #     try:
        #         # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
        #         data_grid_Respuesta = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))
        #         with transaction.atomic():
        #             # Guarda cabecera y detalle
        #             cabecera = form.save(commit=False)
        #             usuario_actual = self.request.session['AIGN_USERID']
        #             cabecera.usuario_actual = usuario_actual
        #             cabecera.save()
        #             # print('CABECERAAAAAAAAAAAAA ', cabecera.pk)
        #             for index, row in data_grid_Respuesta.iterrows():
        #                 tab_respuesta = Gen_Respuesta()
        #                 # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
        #                 if 'res_id' in data_grid_Respuesta:
        #                     # Si se edita, es decir si existe un valor
        #                     if not pd.isna(row.res_id):
        #                         print('MULTIMPORTANTE1.2 ', row.res_id, row.res_respuesta,
        #                               row.res_escorrecta)
        #                         tab_respuesta.res_id = row.res_id
        #                         tab_respuesta.cart_id = cabecera.pk
        #                         tab_respuesta.res_respuesta = row.res_respuesta
        #                         tab_respuesta.res_escorrecta = row.res_escorrecta
        #                         tab_respuesta.res_estado = 0 if row._action == 'E' else 1
        #                         # EN CASO DE ELIMINAR UN REGISTRO DE LA GRILLA AL EDITAR
        #                         if tab_respuesta.res_estado == 0:
        #                             tab_multimedia = Gen_Multimedia()
        #                             with transaction.atomic():
        #                                 # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
        #                                 # el pk desde el metodo dispach
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(
        #                                         """SELECT mul_archivo FROM gen.multimedia
        #                                            WHERE cart_id = %s AND res_id = %s""",
        #                                         [self.kwargs['pk'], tab_respuesta.res_id])
        #                                     result = cursor.fetchall()
        #                                     if result:
        #                                         imagen_url = result[0]
        #                                         # print(imagen_url)
        #                                     else:
        #                                         imagen_url = None
        #
        #                                 # print(self.kwargs['pk'])
        #                                 # print(self.get_object())
        #                                 with connection.cursor() as cursor:
        #                                     cursor.execute(
        #                                         """delete from gen.multimedia
        #                                           where cart_id = %s AND res_id = %s""",
        #                                         [self.kwargs['pk'], tab_respuesta.res_id])
        #
        #                                 if imagen_url:
        #                                     # print('existe_imagen')
        #                                     for row in result:
        #                                         # print(row[0])
        #                                         imagen_url = row[0]
        #                                         file_path = os.path.join(settings.MEDIA_ROOT,
        #                                                                  imagen_url[len(settings.MEDIA_URL):])
        #                                         # print('yeyyyy ', file_path)
        #                                         if os.path.exists(file_path):
        #                                             os.remove(file_path)
        #
        #                     else:
        #                         print('MULTIMPORTANTE1.3 ', row.res_id, row.res_respuesta,
        #                               row.res_escorrecta)
        #                         tab_respuesta.cart_id = cabecera.pk
        #                         tab_respuesta.res_respuesta = row.res_respuesta
        #                         tab_respuesta.res_escorrecta = row.res_escorrecta
        #                         tab_respuesta.save()
        #                         if not pd.isna(row.mul_archivo):
        #                             tab_multimedia = Gen_Multimedia()
        #                             tema_actividad = Gen_TemaActividad.objects.get(tac_id=cabecera.tac_id)
        #                             tab_multimedia.tem_id = tema_actividad.tem_id
        #                             tab_multimedia.act_id = tema_actividad.act_id
        #                             tab_multimedia.res_id = tab_respuesta.res_id
        #                             tab_multimedia.cart_id = cabecera.pk
        #                             tab_multimedia.mul_archivo = row.mul_archivo
        #                             tab_multimedia.mul_tipo = row.mul_tipo
        #                             tab_multimedia.mul_formato = row.mul_formato
        #                             # print('arch ', row.mul_archivo)
        #                             # print('tip ', row.mul_tipo)
        #                             # print('for ', row.mul_formato)
        #                             tab_multimedia.save()
        #                 else:
        #                     print('MULTIMPORTANTE1.4 ', row.res_respuesta,
        #                           row.res_escorrecta)
        #                     tab_respuesta.cart_id = cabecera.pk
        #                     tab_respuesta.res_respuesta = row.res_respuesta
        #                     tab_respuesta.res_escorrecta = row.res_escorrecta
        #                     tab_respuesta.save()
        #                     if not pd.isna(row.mul_archivo):
        #                         tab_multimedia = Gen_Multimedia()
        #                         tema_actividad = Gen_TemaActividad.objects.get(tac_id=cabecera.tac_id)
        #                         tab_multimedia.tem_id = tema_actividad.tem_id
        #                         tab_multimedia.act_id = tema_actividad.act_id
        #                         tab_multimedia.res_id = tab_respuesta.res_id
        #                         tab_multimedia.cart_id = cabecera.pk
        #                         tab_multimedia.mul_archivo = row.mul_archivo
        #                         tab_multimedia.mul_tipo = row.mul_tipo
        #                         tab_multimedia.mul_formato = row.mul_formato
        #                         tab_multimedia.save()
        #                 tab_respuesta.save()
        #             messages.success(request, CRUD_MSG.CREATE)
        #             return JsonResponse(r)
        #     except django.db.models.query_utils.InvalidQuery as e:
        #         extra_errors.append(str(e))
        #
        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:

                identificador_carta = -1
                with transaction.atomic():
                    with transaction.atomic():

                        for index, row in data_grid_multimedia.iterrows():
                            cart_id = row['cart_id']
                            muar_id = row['muar_id']

                            identificador_carta = cart_id
                            print('cart_id', cart_id)
                            print('muar_id', muar_id)
                            # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                            # el pk desde el metodo dispach

                            with connection.cursor() as cursor:
                                cursor.execute(
                                    """
                                    delete from gen.carta_mult
                                    where carta_mult.camu_cart_id = %s
                                    """,
                                    [cart_id])

                            with connection.cursor() as cursor:
                                cursor.execute(
                                    """ SELECT muar_ruta  
                                        FROM postgres.gen.multimedia_archivos ma 
                                        WHERE ma.muar_id = %s""",
                                    [muar_id])
                                result = cursor.fetchall()

                                print('muar ruta', result[0])
                                if result:
                                    ruta_archivo = result[0]
                                else:
                                    ruta_archivo = None


                            with connection.cursor() as cursor:
                                cursor.execute(
                                    """ DELETE
                                        FROM postgres.gen.multimedia_archivos ma
                                        WHERE ma.muar_id = %s""",
                                    [muar_id])

                            #
                            if ruta_archivo:
                                # print('existe_imagen')
                                for row in result:
                                    print(row[0])
                                    ruta_archivo = row[0]
                                    file_path = os.path.join(settings.MEDIA_ROOT, ruta_archivo[len(settings.MEDIA_URL):])
                                    print('ruta archivo ', file_path)
                                    if os.path.exists(file_path):
                                        os.remove(file_path)

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
            cart_id = _e.decrypt(context['pk'])
        else:
            cart_id = context['object'].cart_id

        print('el cart id', cart_id)
        ret.append(get_genMultimediaFileDetsForm(cart_id).to_JSON())
        # ret.append(get_genMultimediaDetsForm(cart_id).to_JSON())
        context['grids_detalles'] = ret
        # print('15')
        return context

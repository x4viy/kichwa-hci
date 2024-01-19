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
class Gen_SesionJuegoListView(ListView):
    model = Gen_SesionJuego
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
            return Gen_SesionJuego.objects.all()
        if rol_usuario_actual in [1, 2]:
            # Filtra los temas según el usuario_actual y rol_usuario_actual
            return Gen_SesionJuego.objects.filter(aud_uc=usuario_actual)
        else:
            return Gen_SesionJuego.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name_plural
        context['url_form'] = reverse_lazy('multimedia_game:gen_ses_jue_add')  # add
        context['url_form_add'] = reverse_lazy('multimedia_game:gen_ses_jue_add')  # add
        context['url_form_edit'] = 'multimedia_game:gen_ses_jue_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'seju_introduccion': None,
                                  'seju_codigo': None,
                                  'seju_tip_id': None,
                                }
        # encriptacion del id
        for r in context['object_list']:
            r.seju_id = _e.encrypt(r.seju_id)
        return context


# Autor: Bryan Amaya
# Agregar
class Gen_SesionJuegoCreateView(CreateView):
    model = Gen_SesionJuego
    form_class = Gen_SesionJuegoForm
    template_name = 'sesion-juego/form-sesion-juego.html'
    success_url = reverse_lazy('multimedia_game:gen_ses_jue_list')

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
        kwargs = super(Gen_SesionJuegoCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
    def get_initial(self):
        rol_id = self.request.session['AIGN_ROLID']
        usuario_id = self.request.session['AIGN_USERID']
        return {'rol_id': rol_id, 'usuario_id': usuario_id}


    def loadDataToTable(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT cc.carca_id AS IDENTIFICADOR ,c.cart_id AS IDENTIFICADOR_CARTA,c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, 
                    ma.muar_tipo AS TIPO, c2.cat_nombre AS CATEGORIA, c2.cat_id AS IDENTIFICADOR_CATE
                    FROM gen.carta c 
                    INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id = c.cart_id 
                    INNER JOIN gen.categoria c2 ON c2.cat_id = cc.carca_cat_id 
                    INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                    INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                    WHERE c.cart_estado = 1""",
                )
            return cursor.fetchall()

    def find_cartas_seleccionadas(self, resultado_post, cabecera):

        if 'numero-cartas' in resultado_post:

            valores_cartas = resultado_post['numero-cartas']

            # Utiliza el método split para dividir la cadena por el carácter "-"
            numeros = valores_cartas.split("-")

            # Filtra los elementos no vacíos (por si hay un guion al final)
            identificadores_carta_categoria = [int(numero) for numero in numeros if numero]


            for numero_carta_categoria in identificadores_carta_categoria:

                carta_categoria = Gen_CartaCategoria.objects.filter(carca_id=numero_carta_categoria)

                for carta_categoria_usada_sesion in carta_categoria:

                    cart_cate_ses = Gen_CartaCategoriaSesion()
                    cart_cate_ses.ccs_carca_id = carta_categoria_usada_sesion
                    cart_cate_ses.ccs_seju_id = cabecera
                    cart_cate_ses.save()


    # Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}
        print('ENTRE AL CREAR')

        # Crear el registro
        if 'CONSULT_CATE' in request.POST:

            tipo = json.loads(request.POST['tip'])
            if tipo != "5" and tipo != "6":
                return JsonResponse(r)

            r['datos_tabla'] = self.loadDataToTable()
            return JsonResponse(r)

        elif 'CREATE' in request.POST and form.is_valid():
            try:
                print("adentro   ", request.POST)
                print("cabeza   ", form)

                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()

                    resultado_post = request.POST

                    print('ultimo ingresado',cabecera.seju_id)
                    self.find_cartas_seleccionadas(resultado_post, cabecera)

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
        ret = []
        ret.append(get_genCartaDetsForm(None).to_JSON())
        print('ret  ', get_genCartaDetsForm(None).to_JSON())
        context['grids_detalles'] = ret
        # print('8')
        return context


# Autor: Bryan Amaya
# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Gen_SesionJuegoUpdateView(UpdateView):
    model = Gen_SesionJuego
    form_class = Gen_SesionJuegoForm
    template_name = 'sesion-juego/form-sesion-juego.html'
    success_url = reverse_lazy('multimedia_game:gen_ses_jue_list')

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
        kwargs = super(Gen_SesionJuegoUpdateView, self).get_form_kwargs()
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

    def loadDataToTable(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT cc.carca_id AS IDENTIFICADOR ,c.cart_id AS IDENTIFICADOR_CARTA,c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, 
                    ma.muar_tipo AS TIPO, c2.cat_nombre AS CATEGORIA, c2.cat_id AS IDENTIFICADOR_CATE
                    FROM gen.carta c 
                    INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id = c.cart_id 
                    INNER JOIN gen.categoria c2 ON c2.cat_id = cc.carca_cat_id 
                    INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                    INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                    WHERE c.cart_estado = 1""",
                )
            return cursor.fetchall()

    def loadCartasToTable(self, seju_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT cc.carca_id AS IDENTIFICADOR ,c.cart_id AS IDENTIFICADOR_CARTA,c.cart_descripcion AS DESCRIPCION, ma.muar_ruta AS RUTA, 
                    ma.muar_tipo AS TIPO, c2.cat_nombre AS CATEGORIA, c2.cat_id AS IDENTIFICADOR_CATE
                    FROM gen.carta c 
                    INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id = c.cart_id 
                    INNER JOIN gen.categoria c2 ON c2.cat_id = cc.carca_cat_id 
                    INNER JOIN gen.carta_mult cm ON cm.camu_cart_id = c.cart_id
                    INNER JOIN gen.multimedia_archivos ma ON ma.muar_id = cm.camu_muar_id 
                    INNER JOIN gen.cart_cate_sesion ccs ON ccs.ccs_carca_id = cc.carca_id 
                    INNER JOIN gen.sesion_juego sj ON sj.seju_id = ccs.ccs_seju_id 
                    WHERE c.cart_estado = 1 and sj.seju_id =%s""",
                [seju_id])
            return cursor.fetchall()

    def find_cartas_categoria_seleccionadas(self, resultado_post, cabecera):

        if 'numero-cartas' in resultado_post:

            # Utiliza el método split para dividir la cadena por el carácter "-"
            numeros = resultado_post['numero-cartas'].split("-")

            # Filtra los elementos no vacíos (por si hay un guion al final)
            identificadores_cartas_categoria_sesion = [int(numero) for numero in numeros if numero]

            print('identificadores_cartas ', len(identificadores_cartas_categoria_sesion))

            cartas_cate_sesi_comparar = Gen_CartaCategoriaSesion.objects.filter(ccs_seju_id=cabecera.seju_id)

            for carta_cate_sesi_comparar in cartas_cate_sesi_comparar:

                if carta_cate_sesi_comparar.ccs_carca_id_id not in identificadores_cartas_categoria_sesion:
                    carta_cate_sesi_comparar.delete()

                elif len(identificadores_cartas_categoria_sesion) == 0:
                    carta_cate_sesi_comparar.delete()

                elif carta_cate_sesi_comparar.ccs_carca_id_id in identificadores_cartas_categoria_sesion:
                    identificadores_cartas_categoria_sesion.remove(carta_cate_sesi_comparar.ccs_carca_id_id)

            if len(identificadores_cartas_categoria_sesion) == 0:
                return

            for identificador_carta_categoria in identificadores_cartas_categoria_sesion:
                cartas_categoria = Gen_CartaCategoria.objects.filter(carca_id=identificador_carta_categoria)

                for carta_cate_usada_sesion in cartas_categoria:
                    cart_cate_ses = Gen_CartaCategoriaSesion()
                    cart_cate_ses.ccs_carca_id = carta_cate_usada_sesion
                    cart_cate_ses.ccs_seju_id = cabecera
                    cart_cate_ses.save()

    #Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}

        print("adentro   ", request.POST)
        #print("json   ", pd.DataFrame(json.loads(request.POST['multimedia_file_grid'])))

        #data_grid_multimedia = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))

        if 'CONSULT_CATE' in request.POST:

            tipo = json.loads(request.POST['tip'])
            if tipo != "5" and tipo != "6":
                return JsonResponse(r)

            r['datos_tabla'] = self.loadDataToTable()
            r['cartas_seleccionada'] = self.loadCartasToTable(self.kwargs['pk'])
            return JsonResponse(r)

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
                    resultado_post = request.POST
                    self.find_cartas_categoria_seleccionadas(resultado_post, cabecera)
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
            seju_id = _e.decrypt(context['pk'])
        else:
            seju_id = context['object'].seju_id

        print('el seju_id', seju_id)
        ret.append(get_genCartaDetsForm(seju_id).to_JSON())
        # ret.append(get_genMultimediaDetsForm(cart_id).to_JSON())
        context['grids_detalles'] = ret
        # print('15')
        return context

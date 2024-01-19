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
            'cart_traduccion': None,

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


    def find_categorias_seleccionadas(self, resultado_post, cabecera):

        if 'numero-categorias' in resultado_post:

            valores_cartas = resultado_post['numero-categorias']

            # Utiliza el método split para dividir la cadena por el carácter "-"
            numeros = valores_cartas.split("-")

            # Filtra los elementos no vacíos (por si hay un guion al final)
            numeros = [int(numero) for numero in numeros if numero]

            for numero_categoria in numeros:

                categoria = Gen_Categoria.objects.filter(cat_id=numero_categoria)

                for categoria_carta in categoria:

                    cart_cate = Gen_CartaCategoria()

                    cart_cate.carca_cat_id = categoria_carta
                    cart_cate.carca_cart_id = cabecera

                    cart_cate.save()

    def loadDataToTable(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT c.cat_id as IDENTIFICADOR, c.cat_nombre AS NOMBRE, c.cat_descripcion AS DESCRIPCION  
                    from gen.categoria c """,
                )
            return cursor.fetchall()

    # Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}
        print('ENTRE AL CREAR')
        # Crear el registro
        if 'CONSULT_CATEGORIA' in request.POST:
            r['datos_tabla'] = self.loadDataToTable()
            return JsonResponse(r)

        elif 'CREATE' in request.POST and form.is_valid():
            try:
                print("adentro   ", request.POST)
                print("cabeza   ", form)
                archivo_imagen = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))
                with transaction.atomic():
                    # Guarda cabecera con commit false, esto con el objetivo
                    # de poder acceder a los datos con los que se guardaria en la base
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    resultado_post = request.POST

                    print('ultimo ingresado', cabecera.cart_id)
                    self.find_categorias_seleccionadas(resultado_post, cabecera)
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

    def loadDataToTable(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT c.cat_id as IDENTIFICADOR, c.cat_nombre AS NOMBRE, c.cat_descripcion AS DESCRIPCION  
                    from gen.categoria c """,
                )
            return cursor.fetchall()

    def loadCategoriasToTable(self,cart_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT  c2.cat_id AS IDENTIFICADOR, c2.cat_nombre AS NOMBRE, c2.cat_descripcion AS DESCRIPCION
                    FROM gen.carta c 
                    INNER JOIN gen.carta_categoria cc ON cc.carca_cart_id = c.cart_id 
                    INNER JOIN gen.categoria c2 ON c2.cat_id = cc.carca_cat_id 
                    WHERE c.cart_id = %s """,
                [cart_id])
            return cursor.fetchall()

    def find_categorias_seleccionadas(self, resultado_post, cabecera):

        if 'numero-categorias' in resultado_post:

            # Utiliza el método split para dividir la cadena por el carácter "-"
            numeros = resultado_post['numero-categorias'].split("-")


            # Filtra los elementos no vacíos (por si hay un guion al final)
            identificadores_categoria = [int(numero) for numero in numeros if numero]

            cartas_cate_comparar = Gen_CartaCategoria.objects.filter(carca_cart_id=cabecera.cart_id)

            for carta_cate_comparar in cartas_cate_comparar:

                if carta_cate_comparar.carca_cat_id_id not in identificadores_categoria:
                    carta_cate_comparar.delete()

                elif len(identificadores_categoria) == 0:
                    carta_cate_comparar.delete()

                elif carta_cate_comparar.carca_cat_id_id in identificadores_categoria:
                    identificadores_categoria.remove(carta_cate_comparar.carca_cat_id_id)

            if len(identificadores_categoria) == 0:
                return

            for identificador_categoria in identificadores_categoria:
                categoria = Gen_Categoria.objects.filter(cat_id=identificador_categoria)

                for categoria_carta in categoria:
                    cart_cate = Gen_CartaCategoria()

                    cart_cate.carca_cat_id = categoria_carta
                    cart_cate.carca_cart_id = cabecera
                    cart_cate.save()

    #Autor: Bryan Amaya
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True
        r = {'a': 1}

        print("adentro   ", request.POST)
        #print("adentro   ", request.POST['multimedia_file_grid'])
        #print("json   ", pd.DataFrame(json.loads(request.POST['multimedia_file_grid'])))

        # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.

        if 'CONSULT_CATEGORIA' in request.POST:
            r['datos_tabla'] = self.loadDataToTable()
            r['categorias_seleccionada'] = self.loadCategoriasToTable(self.kwargs['pk'])
            return JsonResponse(r)
        # Editar
        elif 'SAVE' in request.POST and form.is_valid():
            try:
                data_grid_multimedia = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))

                with transaction.atomic():
                    # Guarda cabecera y detalle
                    cabecera = form.save(commit=False)
                    usuario_actual = self.request.session['AIGN_USERID']
                    cabecera.usuario_actual = usuario_actual
                    cabecera.save()
                    resultado_post = request.POST
                    self.find_categorias_seleccionadas(resultado_post,cabecera)
                    # print('CABECERAAAAAAAAAAAAA ', cabecera.pk)
                    for index, row in data_grid_multimedia.iterrows():
                        carta = Gen_Carta()
                        tab_archivos_multimedia = Gen_MultimediaFile()
                        # Valida si el registro ingresado es uno nuevo, o es uno existente que fue modificado
                        if 'muar_id' in data_grid_multimedia:
                            # Si se edita, es decir si existe un valor
                            if not pd.isna(row.muar_id):
                                tab_archivos_multimedia.muar_estado = 0 if row._action == 'E' else 1
                                tab_archivos_multimedia.muar_id = row.muar_id

                                # EN CASO DE ELIMINAR UN REGISTRO DE LA GRILLA AL EDITAR
                                if tab_archivos_multimedia.muar_estado == 0:
                                    with transaction.atomic():
                                        # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                                        # el pk desde el metodo dispach
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                """SELECT muar_ruta FROM gen.multimedia_archivos
                                                   WHERE muar_id = %s""",
                                                [tab_archivos_multimedia.muar_id])

                                            result = cursor.fetchall()
                                            if result:
                                                imagen_url = result[0]
                                                # print(imagen_url)
                                            else:
                                                imagen_url = None


                                        # print(self.get_object())
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                """delete from gen.carta_mult            
                                                   where carta_mult.camu_muar_id = %s""",
                                                [tab_archivos_multimedia.muar_id])

                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                """ DELETE FROM postgres.gen.multimedia_archivos ma
                                                    WHERE ma.muar_id = %s""",
                                                [tab_archivos_multimedia.muar_id])

                                        if imagen_url:
                                            # print('existe_imagen')
                                            for row in result:
                                                # print(row[0])
                                                imagen_url = row[0]
                                                file_path = os.path.join(settings.MEDIA_ROOT,
                                                                         imagen_url[len(settings.MEDIA_URL):])
                                                if os.path.exists(file_path):
                                                    os.remove(file_path)


##desde aqui
                            else:
                                carta.cart_id = row.cart_id
                                carta.cart_descripcion = row.cart_descripcion
                                carta.cart_traduccion = row.cart_traduccion
                                carta.save()
                        else:
                            carta.cart_id = row.cart_id
                            carta.cart_descripcion = row.cart_descripcion
                            carta.cart_traduccion = row.cart_traduccion
                            carta.save()

                    messages.success(request, CRUD_MSG.CREATE)
                    return JsonResponse(r)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                data_grid_multimedia = pd.DataFrame(json.loads(request.POST['multimedia_file_grid']))

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

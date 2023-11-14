# Autor: Dre
# Fecha: 17/12/2022 010:00
# Descripción: Vista para la opción categorias.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar
import json
import os

import django.db.models.query_utils
import pandas as pd
from django.db import transaction, connection
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.middleware import csrf
from django.shortcuts import redirect
#
_e = EncryptDES()

import json
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import datetime


# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file_name = request.POST.get('myfile', '')
#         file_data = request.POST.get('myfile', '')
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#         print('INTERESANTE: ',file_path)
#         with open(file_path, 'wb+') as f:
#             f.write(file_data.encode())
#         return JsonResponse({'status': 'success'})
@csrf_exempt
def upload_file(request):
    print(request.FILES)
    if request.method == 'POST' and 'mul_archivo' in request.FILES:
        myfile = request.FILES['mul_archivo']
        extension_archivo = os.path.splitext(myfile.name)[1]  # obteniendo la extensión
        fs = FileSystemStorage()
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + extension_archivo
        fecha_hora_actual = fecha_hora_actual.replace(':', '-')  # Reemplazar los dos puntos con guiones
        fecha_hora_actual = fecha_hora_actual.replace(' ', '_')  # Reemplazar los espacios en blanco con guiones bajos
        # print(fecha_hora_actual)
        filename = fs.save(fecha_hora_actual, myfile)
        # Utiliza os.path.splitext para obtener la extensión del archivo
        extension = os.path.splitext(filename)[1]

        # Imprime la extensión del archivo
        # print('La extensión del archivo es:', extension)
        uploaded_file_url = fs.url(filename)
        # print(myfile, fs, filename, uploaded_file_url)
        # print('soydiospelado ', filename)
        return JsonResponse({'success': True, 'url': uploaded_file_url})
    else:
        # print('algoandamal')
        return JsonResponse({'success': False, 'error': 'No se ha enviado ningún archivo'})


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        file_url = request.POST.get('file_url')
        # print('vivalavidapelaoestoyeliminando ', file_url)
        # Verifica que la URL del archivo sea válida
        if file_url:
            # print('entresantamaria')
            # Elimina el archivo del sistema de archivos
            print(os.path)
            mediaurl = '/media/' + file_url
            fs = FileSystemStorage()
            # print('AMENODORIME', mediaurl)
            file_path = os.path.join(settings.MEDIA_ROOT, file_url)
            # print(file_path)
            fs.delete(file_path)
            mult = Gen_Multimedia.objects.filter(mul_archivo=mediaurl)
            # print('jeje')
            if mult.exists():
                # print('EEE ', mult[0].mul_id)
                mult[0].mul_estado = 0
                mult[0].save()
            return JsonResponse({'success': True, 'error': 'Eliminado'})
        else:
            return JsonResponse({'success': False, 'error': 'No eliminado'})


# Listar
class Gen_ActividadListView(ListView):
    model = Gen_Actividad
    template_name = 'gen_actividad/list.html'

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Gen_Actividad.objects.filter(act_estado=1)
        return Gen_Actividad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_actividad_add')  # add
        context['url_form_add'] = reverse_lazy('gen:gen_actividad_add')  # add
        context['url_form_edit'] = 'gen:gen_actividad_edit'  # edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {  # 'tem': None,
            'act_nombre': None,
            'act_descripcion': None,
        }
        # # ecriptacion del id
        print('3')
        for r in context['object_list']:
            r.act_id = _e.encrypt(r.act_id)
        return context


# Agregar
class Gen_ActividadCreateView(CreateView):
    model = Gen_Actividad
    form_class = Gen_ActividadForm
    template_name = 'gen_actividad/form.html'
    success_url = reverse_lazy('gen:gen_actividad_list')

    # Asigna al kwargs la variable de session desde el formulario

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(Gen_ActividadCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # Iniciallizar el formulario
    def get_initial(self):
        mul_id = self.request.session.get('AIGN_MUL_ID')
        multimedia = Gen_Multimedia.objects.filter(mul_id=mul_id)
        return {'mul_id': self.request.session.get('AIGN_MUL_ID')}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True

        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:
                cabecera = form.save(commit=False)
                # cabecera.save()
                formcomp = Gen_ActividadForm(request.POST, request.FILES)
                if formcomp.is_valid():
                    Centinela = True
                    # Imprimir datos del formulario en consola
                    # print(formcomp.cleaned_data['usu_id'])
                    # print('MULTIMEDIAACTIVIDADDDDDDDDDDDDDDDDDDDDDDDD')
                    # print(formcomp.cleaned_data['asi'])
                    # print(formcomp.cleaned_data['act_nombre'])
                    # print(formcomp.cleaned_data['mul_id'])
                    # print(formcomp.cleaned_data['act_descripcion'])
                    if formcomp.cleaned_data.get('mul_archivo', None):
                        # print('XDD', formcomp.cleaned_data['mul_archivo'])
                        tab_multimedia = Gen_Multimedia()
                        archivo = formcomp.cleaned_data['mul_archivo']
                        ext = os.path.splitext(archivo.name)
                        # print('FORMATO ', ext[1])

                        if archivo.size > 10 * 1024 * 1024:  # 10 MB in bytes
                            form.add_error('mul_archivo', ('El tamaño del archivo no debe exceder 10 MB.'))
                            Centinela=False
                        elif ext[1].lower() != '.png' and ext[1].lower() != '.jpg':
                            # print('qpd' , ext[1])
                            # if ext[1] == '.png':
                            #     print('spspeld')
                            form.add_error('mul_archivo', ('Solo se aceptan imágenes jpg o png.'))
                            Centinela=False
                        else:
                            # print('kha')
                            Centinela = True
                            cabecera.save()
                            tab_multimedia.act_id = cabecera.pk
                            # fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ext[1]
                            # fecha_hora_actual = fecha_hora_actual.replace(':', '-')  # Reemplazar los dos puntos con guiones
                            # fecha_hora_actual = fecha_hora_actual.replace(' ', '_')  # Reemplazar los espacios en blanco con guiones bajos
                            # print('ArchivoFecha: ', fecha_hora_actual)
                            tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                            tab_multimedia.mul_tipo = 'Imagen'
                            tab_multimedia.mul_formato = ext[1]
                            tab_multimedia.save()
                if Centinela == True:
                    # print('como')
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
class Gen_ActividadUpdateView(UpdateView):
    model = Gen_Actividad
    form_class = Gen_ActividadForm
    template_name = 'gen_asignatura/form.html'
    success_url = reverse_lazy('gen:gen_actividad_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            return redirect('/300/usuario/list/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_ActividadUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        for k in self.kwargs.keys():
            self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        multimedia = Gen_Multimedia.objects.filter(act_id=self.kwargs['pk']).only('mul_id')
        archivo = Gen_Multimedia.objects.filter(act_id=self.kwargs['pk']).only('mul_archivo')

        if multimedia.exists():
            print('URGENTE1 ', multimedia[0].mul_id)
            print('URGENTE2 ', archivo[0].mul_archivo)
            return {'mul_id': multimedia[0].mul_id, 'mul_archivo': archivo[0].mul_archivo}
            # return {'mul_id': multimedia[0].mul_id, 'mul_archivo_existente': archivo[0].mul_archivo}
        return {}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        r = {'a': 1}

        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            try:
                cabecera = form.save(commit=False)
                cabecera.save()
                formcomp = Gen_ActividadForm(request.POST, request.FILES)
                if formcomp.is_valid():
                    # Imprimir datos del formulario en consola
                    # print(formcomp.cleaned_data['usu_id'])
                    # print(formcomp.cleaned_data['cat'])
                    print(formcomp.cleaned_data['act_nombre'])
                    print(formcomp.cleaned_data['act_descripcion'])
                    print('queondaa ', formcomp.cleaned_data['mul_id'])
                    # Si existe un mul id, es decir hay una imagen cargada
                    if formcomp.cleaned_data.get('mul_id', None):
                        # Si existe un archivo nuevo, es decir se quiere modificar la imagen
                        if formcomp.cleaned_data.get('mul_archivo', None):
                            print('XDXDXDXD', formcomp.cleaned_data['mul_id'])
                            print('Xmmmmmmmmmmmmmmmmmmmmmm', formcomp.cleaned_data['mul_archivo'])
                            tab_multimedia = Gen_Multimedia.objects.get(mul_id=formcomp.cleaned_data['mul_id'])
                            print('name ', tab_multimedia.mul_archivo.name)
                            # print(tab_multimedia.mul_archivo.path)
                            file_path = os.path.join(settings.MEDIA_ROOT,
                                                     tab_multimedia.mul_archivo.name[len(settings.MEDIA_URL):])
                            print('avemaria ', file_path)
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            print('xcdddddddddddddddddddd')
                            archivo = formcomp.cleaned_data['mul_archivo']
                            ext = os.path.splitext(archivo.name)
                            print('FORMATO ', ext[1])
                            # tab_multimedia.tem_id = cabecera.pk
                            # fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ext[1]
                            # fecha_hora_actual = fecha_hora_actual.replace(':', '-')  # Reemplazar los dos puntos con guiones
                            # fecha_hora_actual = fecha_hora_actual.replace(' ', '_')  # Reemplazar los espacios en blanco con guiones bajos
                            tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                            # tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                            tab_multimedia.mul_tipo = 'Imagen'
                            tab_multimedia.mul_formato = ext[1]
                            tab_multimedia.save()
                            # tab_multimedia.mul_archivo = fecha_hora_actual
                            # tab_multimedia.save()

                        # Si no existe un archivo nuevo, es decir se buscan modificar cosas que no tienen que ver con la imagen
                        else:
                            tab_multimedia = Gen_Multimedia.objects.get(mul_id=formcomp.cleaned_data['mul_id'])
                            tab_multimedia.mul_archivo = tab_multimedia.mul_archivo
                            tab_multimedia.mul_tipo = tab_multimedia.mul_tipo
                            tab_multimedia.mul_formato = tab_multimedia.mul_formato
                            tab_multimedia.save()
                    # Si no existe un archivo previo y se quiere agregar uno nuevo.
                    elif formcomp.cleaned_data.get('mul_archivo', None):
                        print('XDXDXDXD2', formcomp.cleaned_data['mul_id'])
                        print('XDXDXDXD2', formcomp.cleaned_data['mul_archivo'])
                        tab_multimedia = Gen_Multimedia()
                        archivo = formcomp.cleaned_data['mul_archivo']
                        ext = os.path.splitext(archivo.name)
                        print('FORMATO2 ', ext[1])
                        tab_multimedia.act_id = cabecera.pk
                        tab_multimedia.mul_archivo = form.cleaned_data['mul_archivo']
                        tab_multimedia.mul_tipo = 'Imagen'
                        tab_multimedia.mul_formato = ext[1]
                        tab_multimedia.save()
                form.save()
                messages.success(request, CRUD_MSG.SAVE)
                return HttpResponseRedirect(self.success_url)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                print('DELETEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                print(self.get_object())
                print(self.kwargs['pk'])
                # Aqui se invoca a la grid para obtener los datos que se encuentran en ella.
                # data_grid_Actividad = pd.DataFrame(json.loads(request.POST['actividad_grid']))
                with transaction.atomic():
                    # Elimina de detalle. Se usa el Kwargs, que es el arreglo donde se almacena
                    # el pk desde el metodo dispach
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """SELECT mul_archivo FROM gen.multimedia
                               WHERE act_id = %s""",
                            [self.kwargs['pk']])
                        result = cursor.fetchone()
                        if result:
                            imagen_url = result[0]
                        else:
                            imagen_url = None

                    print(self.kwargs['pk'])
                    print(self.get_object())
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """delete from gen.multimedia
                              where act_id = %s""",
                            [self.kwargs['pk']])
                    print(self.kwargs['pk'])
                    print(self.get_object())
                    # with connection.cursor() as cursor:
                    #     cursor.execute(
                    #         """delete from gen.actividad
                    #           where act_id = %s""",
                    #         [self.kwargs['pk']])
                    # Se elimina la cabecera
                    print(self.kwargs['pk'])
                    print(self.get_object())
                    print('que paso?')
                    print(self.get_object())
                    print('huh?')
                    self.get_object().delete()
                    if imagen_url:
                        print('existe_imagen')
                        print(imagen_url)
                        file_path = os.path.join(settings.MEDIA_ROOT, imagen_url[len(settings.MEDIA_URL):])
                        print(file_path)
                        if os.path.exists(file_path):
                            os.remove(file_path)

                    print('sigue')
                    print('sigue2')
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

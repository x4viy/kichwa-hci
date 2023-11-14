# Autor: Bryan Amaya
# Fecha: 31/05/2023
# Descripción: Vista para la opción tipo.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar
from django.db import transaction
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
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import datetime
#
_e = EncryptDES()


# Listar
class Gen_TipoListView(ListView):
    model = Gen_Tipo
    template_name = 'gen_tipo/list.html'

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return redirect('/')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        emp_filter = self.request.session.get('AIGN_EMP_ID')
        if emp_filter:
            return Gen_Tipo.objects.filter(tip_estado=1)
        return Gen_Tipo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('gen:gen_tipo_add') #add
        context['url_form_add'] = reverse_lazy('gen:gen_tipo_add') #add
        context['url_form_edit'] = 'gen:gen_tipo_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'tip_codigo': None,
                                  'tip_nombre': None,
                                  'tip_descripcion': None}
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.tip_id)
        return context


# Agregar
class Gen_TipoCreateView(CreateView):
    model = Gen_Tipo
    form_class = Gen_TipoForm
    template_name = 'gen_tipo/form.html'
    success_url = reverse_lazy('gen:gen_tipo_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return redirect('/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_TipoCreateView, self).get_form_kwargs()
        # #Roles
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session.get('AIGN_EMP_ID')})
        return kwargs

    # # Iniciallizar el formulario
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
                formcomp = Gen_TipoForm(request.POST, request.FILES)
                if formcomp.is_valid():
                    Centinela = True
                    # Imprimir datos del formulario en consola
                    # print(formcomp.cleaned_data['usu_id'])
                    # print('MULTIMEDIAACTIVIDADDDDDDDDDDDDDDDDDDDDDDDD')
                    # print(formcomp.cleaned_data['asi'])
                    if formcomp.cleaned_data.get('mul_archivo', None):
                        # print('XDD', formcomp.cleaned_data['mul_archivo'])
                        tab_multimedia = Gen_Multimedia()
                        archivo = formcomp.cleaned_data['mul_archivo']
                        ext = os.path.splitext(archivo.name)
                        # print('FORMATO ', ext[1])

                        if archivo.size > 10 * 1024 * 1024:  # 10 MB in bytes
                            form.add_error('mul_archivo', ('El tamaño del archivo no debe exceder 10 MB.'))
                            Centinela = False
                        elif ext[1].lower() != '.png' and ext[1].lower() != '.jpg':
                            # print('qpd' , ext[1])
                            # if ext[1] == '.png':
                            #     print('spspeld')
                            form.add_error('mul_archivo', ('Solo se aceptan imágenes jpg o png.'))
                            Centinela = False
                        else:
                            # print('kha')
                            Centinela = True
                            cabecera.save()
                            tab_multimedia.tip_id = cabecera.pk
                            print('questapasAAAAAAAAAAAAA ', cabecera)
                            print('questapasAAAAAAAAAAAAA ', cabecera.pk)
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
class Gen_TipoUpdateView(UpdateView):
    model = Gen_Tipo
    form_class = Gen_TipoForm
    template_name = 'gen_tipo/form.html'
    success_url = reverse_lazy('gen:gen_tipo_list')

    def get(self, request, *args, **kwargs):
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return redirect('/')
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Gen_TipoUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        # for k in self.kwargs.keys():
        #     self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def get_initial(self):
        multimedia = Gen_Multimedia.objects.filter(tip_id=self.kwargs['pk']).only('mul_id')
        archivo = Gen_Multimedia.objects.filter(tip_id=self.kwargs['pk']).only('mul_archivo')

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
                formcomp = Gen_TipoForm(request.POST, request.FILES)
                if formcomp.is_valid():
                    # Imprimir datos del formulario en consola
                    # print(formcomp.cleaned_data['usu_id'])
                    # print(formcomp.cleaned_data['cat'])
                    # print(formcomp.cleaned_data['act_nombre'])
                    # print(formcomp.cleaned_data['act_descripcion'])
                    # print('queondaa ', formcomp.cleaned_data['mul_id'])
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
                        tab_multimedia.tip_id = cabecera.pk
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
                               WHERE tip_id = %s""",
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
                              where tip_id = %s""",
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

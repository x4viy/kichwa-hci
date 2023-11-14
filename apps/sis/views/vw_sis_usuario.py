# Autor: emdr
# Fecha: 26/12/2022 010:00
# Descripción: Vista para la opción categorias.
#              En esta opción permite:
#              listar, agregar, modificar, eliminar

import django.db.models.query_utils
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.hashers import make_password, check_password
from apps.authentication.forms import SignUpForm
from apps.sis.forms import Sis_UsuarioForm
from apps.sis.models import Sis_Usuario
from apps.gen.models import *
from apps.gen.forms import *
from vars.js import datatable_opts
from django.contrib import messages
from core.encryption_util import *
from utils import utils
from vars.msg import CRUD_MSG
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
import re
from django.contrib.auth.password_validation import validate_password
#
_e = EncryptDES()


# Listar
class Sis_UsuarioListView(ListView):
    model = User
    template_name = 'sis_usuario/list.html'


    def get(self, request, *args, **kwargs):
        id_usuario_actual = self.request.session['AIGN_USERID']
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return redirect(f'/300/usuario/edit/{id_usuario_actual}/')
        else:
            return super().get(request, *args, **kwargs)


    def get_queryset(self):
        # emp_filter = self.request.session.get('AIGN_EMP_ID')
        # if emp_filter:
        #     return User.objects.filter(usu_estado=1)
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reporte ' + self.model._meta.verbose_name
        context['url_form'] = reverse_lazy('sis:sis_usuario_add') #add
        context['url_form_add'] = reverse_lazy('sis:sis_usuario_add') #add
        context['url_form_edit'] = 'sis:sis_usuario_edit' #edit
        context['datatable_id'] = 'datatable1_id'
        context['datatable_opts'] = datatable_opts
        # Agregar boton 'Agregar' lista
        context['show_fields'] = {'username': None,
                                  'first_name': None,
                                  'last_name': None,
                                  'email': None,
                                  'institucion': None,
                                  'curso': None,
                                  'rol': None,
                                  }
        # # ecriptacion del id
        for r in context['object_list']:
            r.lin_id = _e.encrypt(r.id)
        return context


# Agregar
class Sis_UsuarioCreateView(CreateView):
    model = User
    form_class = Sis_UsuarioForm
    template_name = 'sis_usuario/form.html'
    success_url = reverse_lazy('sis:sis_usuario_list')

    def get(self, request, *args, **kwargs):
        id_usuario_actual = self.request.session['AIGN_USERID']
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            return redirect(f'/300/usuario/edit/{id_usuario_actual}/')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        request.POST._mutable = True

        # print(request.POST)
        # print(form.is_valid())
        # print(form._errors)

        # Crear el registro
        if 'CREATE' in request.POST and form.is_valid():
            try:
                password = form.cleaned_data.get('password')
                password2 = form.cleaned_data.get('password2')

                if password == password2:
                    # Encriptar la contraseña usando make_password
                    hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256')
                    # Actualizar la instancia del modelo con la contraseña encriptada
                    form.instance.password = hashed_password
                    form.save()
                    messages.success(request, CRUD_MSG.CREATE)
                    return HttpResponseRedirect(self.success_url)
                else:
                    form.add_error('password2', 'Las contraseñas no coinciden.')

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
        context['is_edit'] = 0
        return context


# Editar
# Eiminar: Eliminado lógico -> Cambiar campo _estado = 1:Normal / 0: Eliminado
class Sis_UsuarioUpdateView(UpdateView):
    model = User
    form_class = Sis_UsuarioForm
    template_name = 'sis_usuario/form.html'
    success_url = reverse_lazy('sis:sis_usuario_list')
    # print('1')

    def get(self, request, *args, **kwargs):
        id_usuario_actual = self.request.session['AIGN_USERID']
        rol_usuario_actual = self.request.session['AIGN_ROLID']
        id_usuario_url = int(re.search(r'/(\d+)/$', self.request.path).group(1))
        if rol_usuario_actual != 1:
            if rol_usuario_actual != 2:
                return redirect('/')
            if id_usuario_actual != id_usuario_url:
                return redirect(f'/300/usuario/edit/{id_usuario_actual}/')
            else:
                return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

    # Asigna al kwargs la variable de session desde el formulario
    def get_form_kwargs(self):
        kwargs = super(Sis_UsuarioUpdateView, self).get_form_kwargs()
        # kwargs.update({'AIGN_OPCIONES': self.request.session['AIGN_OPCIONES']})
        # kwargs.update({'AIGN_EMP_ID': self.request.session['AIGN_EMP_ID']})
        # print('2')
        # print(kwargs)
        # kwargs['id_temp'] =
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # Desencriptando el pk
        # for k in self.kwargs.keys():
        #     self.kwargs[k] = _e.decrypt(self.kwargs[k])
        self.object = self.get_object()
        # print(self.object.password)
        self.object.password = ''
        # print(self.object.password)
        # print('3')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        usuario = User.objects.filter(id=self.kwargs['pk']).only('id')
        password = User.objects.filter(id=self.kwargs['pk']).only('password')
        nombre_usuario = self.request.session['AIGN_USUARIO']
        rol_id = self.request.session['AIGN_ROLID']

        if usuario.exists():
            # print('IMPORTANTEEEEEEEEEEEEEEEEEEEEE ', usuario[0].username, ' ', nombre_usuario)
            return {'id': usuario[0].id, 'password': password[0].password, 'nombre_usuario': nombre_usuario, 'rol_id': rol_id}
            # return {'mul_id': multimedia[0].mul_id, 'mul_archivo_existente': archivo[0].mul_archivo}
        return {}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra_errors = []
        # print('4')
        # Editar
        # print(request.POST)
        # print(form.is_valid())
        # print(form._errors)
        # Editar
        if 'SAVE' in request.POST and form.is_valid():
            # print('qqq')
            try:
                nueva_password = form.cleaned_data.get('nueva_password')
                password2 = form.cleaned_data.get('password2')
                antigua_password = form.cleaned_data.get('antigua_password')
                # print('.....')
                if nueva_password or antigua_password:
                    # rol_usuario_actual = self.initial.get('rol_id')
                    rol_id = form.initial['rol_id']
                    print('puntosv2 ', rol_id)
                    if rol_id == 2:
                        # print('QUEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                        antigua_password = form.cleaned_data.get('antigua_password')
                        # print('antigua ', antigua_password)
                        # print('nueva ', nueva_password)
                        password_original = form.cleaned_data.get('password')
                        Centinela1 = False
                        Centinela2 = False
                        try:
                            validate_password(nueva_password)
                            Centinela1 = True
                            # print('yuju')
                        except ValidationError as e:
                            Centinela1 = False
                            form.add_error('nueva_password', e)

                        if check_password(antigua_password, password_original):
                            print('Contraseña antigua ingresada correctamente')
                            Centinela2 = True
                            # print('Las contraseñas coinciden:', nueva_password)
                            if Centinela1 is True and Centinela2 is True:
                                hashed_password = make_password(nueva_password, salt=None, hasher='pbkdf2_sha256')
                                # Actualizar la instancia del modelo con la contraseña encriptada
                                form.instance.password = hashed_password
                                form.save()
                                # messages.success(request, CRUD_MSG.SAVE)
                                return HttpResponseRedirect(self.success_url)
                        else:
                            print('Contraseña antigua ingresada erroneamente')
                            Centinela2 = False
                            form.add_error('antigua_password', 'La contraseña ingresada no es correcta.')
                            print(form.errors)

                    if nueva_password == password2 and not antigua_password:
                        Centinela3 = False
                        Centinela4 = False
                        try:
                            validate_password(nueva_password)
                            Centinela3 = True
                            print('yuju')
                        except ValidationError as e:
                            Centinela3 = False
                            form.add_error('nueva_password', e)

                        try:
                            validate_password(password2)
                            Centinela4 = True
                            print('yuju')
                        except ValidationError as e:
                            Centinela4 = False
                            form.add_error('password2', e)

                        if Centinela3 is True and Centinela4 is True:
                            print('se supone que todo bien')
                            print(form.errors)
                            # print('las contraseñas coinciden ', nueva_password, ' ', password2)
                            # Encriptar la contraseña usando make_password
                            hashed_password = make_password(nueva_password, salt=None, hasher='pbkdf2_sha256')
                            # Actualizar la instancia del modelo con la contraseña encriptada
                            form.instance.password = hashed_password
                            form.save()
                            messages.success(request, CRUD_MSG.SAVE)
                            return HttpResponseRedirect(self.success_url)
                    else:
                        form.add_error('password2', 'Las contraseñas no coinciden.')
                else:
                    password_antigua = form.cleaned_data.get('password')
                    form.instance.password = password_antigua
                    form.save()
                    messages.success(request, CRUD_MSG.SAVE)
                    return HttpResponseRedirect(self.success_url)
            except django.db.models.query_utils.InvalidQuery as e:
                extra_errors.append(str(e))

        # Eliminar
        if 'DELETE' in request.POST and form.is_valid():
            try:
                #Aqui instrucción para eliminado form.delete()
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
        usuario = User.objects.filter(id=self.kwargs['pk']).only('id')
        context['page_title'] = self.model._meta.verbose_name
        context['url_list'] = self.success_url
        context['is_edit'] = 1
        context['is_user_actual'] = self.request.session['AIGN_USUARIO']
        context['rol_user_actual'] = self.request.session['AIGN_ROLID']
        context['is_user_editando'] = usuario[0].username
        return context

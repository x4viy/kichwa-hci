# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from ..sis.models import Sis_OpcionRol
from django.db.models import F
import json
from django.contrib.auth import logout
from apps.sis.models import *
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                      PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.views import PasswordResetView
def login_view(request):
    error = False
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()


    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)


            if user is not None:
                login(request, user)
                if user.rol.rol_id == 3:
                    print('logueado?2')
                    print(user.username)
                    request.session['AIGN_USUARIO'] = user.username
                    request.session['AIGN_ROLID'] = user.rol_id
                    request.session['AIGN_USERID'] = user.id
                    return redirect("/")

                elif user.rol.rol_id == 2:
                    login(request, user)
                    menu = list(Sis_OpcionRol.objects.select_related('opc').filter(oro_estado=1,
                                                                                   # rol=self.request.user.rol_id,
                                                                                   # emp=self.request.user.emp.emp_id,
                                                                                   opc__opc_tipo=1).annotate(
                        opc_id_padre=F('opc__opc_idpadre'),
                        opc_nombre=F('opc__opc_nombre'),
                        opc_url=F('opc__opc_url'),
                        opc_icon=F('opc__opc_icono'),
                        opc_menu_tipo=F('opc__opc_tipo'),
                        # opc_menu_sis=F('opc__opc_menu_sis'),
                        # tab_nombre=F('opc__tab_nombre'),
                    ).order_by('opc__opc_orden').values())

                    for item in menu:
                        del item['aud_fc']
                        del item['aud_fm']

                    menu = [item for item in menu if
                                     item.get('opc_url') not in ('/300/rol/list/', '/200/asignatura/list/', '/200/actividad/list/', '/200/tipo/list/', '/300/opcion/list/', '/300/informacion/list/')]

                    urls_to_skip = {'/300/rol/list/', '/200/asignatura/list/', '/200/actividad/list/',
                                    '/300/opcion/list/', '/300/informacion/list/'}

                    seen_urls = set()

                    for item in menu[
                                :]:  # Iterar sobre una copia para evitar problemas al eliminar elementos durante la iteración
                        url = item.get('opc_url')
                        if url and url not in urls_to_skip and url in seen_urls:
                            menu.remove(item)  # Eliminar elementos duplicados
                            # print('removido ', item)
                        else:
                            seen_urls.add(url)
                            # print('zz ', seen_urls)
                    menu = json.loads(json.dumps(menu))

                    opciones = list(Sis_OpcionRol.objects.select_related('opc').filter(oro_estado=1,
                                                                                       # rol=self.request.user.rol_id,
                                                                                       # emp=self.request.user.emp.emp_id,
                                                                                       opc__opc_tipo=2).annotate(
                        opc_id_padre=F('opc__opc_idpadre'),
                        opc_nombre=F('opc__opc_nombre'),
                        opc_url=F('opc__opc_url'),
                        opc_icon=F('opc__opc_icono'),
                        opc_menu_tipo=F('opc__opc_tipo'),
                        # opc_menu_sis=F('opc__opc_menu_sis'),
                        # tab_nombre=F('opc__tab_nombre'),
                    ).order_by('opc__opc_orden').values())

                    opciones = json.loads(json.dumps(opciones))

                    # request.session['AIGN_MODULO'] = modulo

                    request.session['AIGN_MENU'] = menu

                    request.session['AIGN_USUARIO'] = user.username
                    request.session['AIGN_EMAIL'] = user.email
                    request.session['AIGN_ROLID'] = user.rol_id
                    request.session['AIGN_USERID'] = user.id


                    request.session.modified = True

                    # ******************************************************************************************************
                    # ******************************************************************************************************

                    return redirect("/200/asignatura/list/")
                elif user.rol.rol_id == 1:
                    print('logueado?')
                    print(user.username)
                    # nombre_usuario = user
                    # print(nombre_usuario)
                    login(request, user)
                    # ******************************************************************************************************
                    # ******************************************************************************************************
                    # opc_menu_tipo (opc_tipo) = M -> 1 / O -> 2
                    # modulo = list(Sis_OpcionRol.objects.select_related('opc').filter(oro_estado = 1,
                    #                                                                  # rol=self.request.user.rol_id,
                    #                                                                  # emp=self.request.user.emp.emp_id,
                    #                                                                  opc__opc_idpadre=None).annotate(
                    #                                                                 opc_id_padre=F('opc__opc_idpadre'),
                    #                                                                 opc_nombre=F('opc__opc_nombre'),
                    #                                                                 opc_url=F('opc__opc_url'),
                    #                                                                 opc_icon=F('opc__opc_icono'),
                    #                                                                 opc_menu_tipo=F('opc__opc_tipo'),
                    #                                                                 # opc_menu_sis=F('opc__opc_menu_sis'),
                    #                                                                 # tab_nombre=F('opc__tab_nombre'),
                    #                                                                 ).order_by('opc__opc_orden').values())
                    #
                    # modulo = json.loads(json.dumps(modulo))

                    menu = list(Sis_OpcionRol.objects.select_related('opc').filter(oro_estado=1,
                                                                                   # rol=self.request.user.rol_id,
                                                                                   # emp=self.request.user.emp.emp_id,
                                                                                   opc__opc_tipo=1).annotate(
                        opc_id_padre=F('opc__opc_idpadre'),
                        opc_nombre=F('opc__opc_nombre'),
                        opc_url=F('opc__opc_url'),
                        opc_icon=F('opc__opc_icono'),
                        opc_menu_tipo=F('opc__opc_tipo'),
                        # opc_menu_sis=F('opc__opc_menu_sis'),
                        # tab_nombre=F('opc__tab_nombre'),
                    ).order_by('opc__opc_orden').values())

                print('menu ', menu)

                for item in menu:
                    del item['aud_fc']
                    del item['aud_fm']

                urls_to_skip = {'/300/rol/list/', '/200/asignatura/list/', '/200/actividad/list/',
                                '/300/opcion/list/', '/300/informacion/list/'}

                seen_urls = set()

                for item in menu[
                            :]:  # Iterar sobre una copia para evitar problemas al eliminar elementos durante la iteración
                    url = item.get('opc_url')
                    if url and url not in urls_to_skip and url in seen_urls:
                        menu.remove(item)  # Eliminar elementos duplicados
                        # print('removido ', item)
                    else:
                        seen_urls.add(url)
                        # print('zz ', seen_urls)
                menu = json.loads(json.dumps(menu))

                opciones = list(Sis_OpcionRol.objects.select_related('opc').filter(oro_estado=1,
                                                                                   # rol=self.request.user.rol_id,
                                                                                   # emp=self.request.user.emp.emp_id,
                                                                                   opc__opc_tipo=2).annotate(
                    opc_id_padre=F('opc__opc_idpadre'),
                    opc_nombre=F('opc__opc_nombre'),
                    opc_url=F('opc__opc_url'),
                    opc_icon=F('opc__opc_icono'),
                    opc_menu_tipo=F('opc__opc_tipo'),
                    # opc_menu_sis=F('opc__opc_menu_sis'),
                    # tab_nombre=F('opc__tab_nombre'),
                ).order_by('opc__opc_orden').values())


                opciones = json.loads(json.dumps(opciones))
                print('opciones ', opciones)
                # request.session['AIGN_MODULO'] = modulo

                request.session['AIGN_MENU'] = menu

                request.session['AIGN_USUARIO'] = user.username
                request.session['AIGN_EMAIL'] = user.email
                request.session['AIGN_ROLID'] = user.rol_id
                request.session['AIGN_USERID'] = user.id
                request.session.modified = True

                # ******************************************************************************************************
                # ******************************************************************************************************

                return redirect("/200/asignatura/list/")
            else:
                print("NOOOOOOOOOOOOOOOOOOO")
                msg = 'Invalid credentials'
                error = True

        else:
            msg = 'Error validating the form'



    return render(request, "accounts/login.html", {"form": form, "msg": msg, 'user': request.user, "redes": redes, "contact": contact, 'error': error})


def register_user(request):
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=raw_password)

            msg = "User created - please login"
            success = True

            # return redirect("/login")

        else:
            msg = "Se encontraron errores en el formulario o CAPTCHA no válido"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success, "redes": redes, "contact": contact})


# def register_user(request):
#     msg = None
#     success = False
#
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#
#         if form.is_valid():
#             # Captura el valor del rol seleccionado del formulario
#             rol_seleccionado = int(form.cleaned_data.get("rol"))
#
#             # Crea el usuario y establece otros campos
#             user = form.save(commit=False)
#             user.is_active = True  # Por defecto, se asume que el usuario es activo
#             user.save()
#
#             # Autentica al usuario recién creado
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)
#
#             # Convierte el valor seleccionado en una instancia de Sis_Rol
#             sis_rol_instance = Sis_Rol.objects.get(pk=rol_seleccionado)
#
#             # Asigna la instancia de Sis_Rol al campo de rol en el usuario
#             if user and sis_rol_instance:
#                 user.rol = sis_rol_instance
#                 user.save()
#
#             msg = "User created - please login"
#             success = True
#
#             # return redirect("/login/")  # Redirige al usuario después de registrarse
#
#         else:
#             msg = "Se encontraron errores en el formulario o CAPTCHA no válido"
#     else:
#         form = SignUpForm()
#
#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def logout_view(request):
    logout(request)
    return redirect('/')


# Función para reutilizar las consultas
def get_custom_context():
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None

    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()

    return {
        'contact': contact,
        'redes': redes,
    }


class PersonalizedPasswordResetView(PasswordResetView):
    template_name = 'Password_reset/password_reset_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_custom_context())
        return context


class PersonalizedPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'Password_reset/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_custom_context())
        return context


class PersonalizedPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'Password_reset/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_custom_context())
        return context


class PersonalizedPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'Password_reset/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_custom_context())
        return context
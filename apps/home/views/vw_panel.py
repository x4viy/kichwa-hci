from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from apps.gen.models import *
from apps.sis.models import *
from apps.home.forms import UserProfileForm
from django.core.mail import send_mail
@login_required
def perfil(request):
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    context = {'segment': 'perfil','redes': redes,
'contact': contact}
    html_template = loader.get_template('accounts/perfil.html')
    return HttpResponse(html_template.render(context, request))


@login_required
def actualizar_perfil(request):
    if request.method == "POST":
        user = request.user
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redireccionar de nuevo a la página del perfil con un parámetro.
            return HttpResponseRedirect(reverse('home:perfil') + '?updated=true')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/perfil.html', {'form': form})

@login_required
def puntajes(request):
    success = request.session.pop('success', False)
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    user_id = request.user.id
    puntajes_usuario = (
        Gen_Puntaje.objects.filter(aud_um=user_id)
        .select_related('jue')  # Existing related object fetch
        .select_related('tac')  # Fetch related Gen_TemaActividad
        .select_related('tac__tem')  # Fetch related Gen_Tema via Gen_TemaActividad
        .select_related('tac__act')  # Fetch related Gen_Actividad via Gen_TemaActividad
    )
    # Filtrado
    asignatura = request.GET.get('asignatura', '').strip()
    fecha = request.GET.get('fecha')
    puntaje_minimo = request.GET.get('puntaje', 0)  # Valor por defecto de 0 si no se proporciona
    institucion = request.GET.get('institucion', '').strip()
    curso = request.GET.get('curso', '').strip()

    if asignatura:
        asi = Gen_Asignatura.objects.get(asi_id=asignatura)
        puntajes_usuario = puntajes_usuario.filter(pun_materia=asi.asi_nombre)
    if fecha:
        puntajes_usuario = puntajes_usuario.filter(pun_fecha=fecha)
    if puntaje_minimo:
        puntajes_usuario = puntajes_usuario.filter(pun_puntaje__gte=puntaje_minimo)  # Usar __gte para puntaje mínimo

        # Filtrar por institución y curso
    if institucion:
        puntajes_usuario = puntajes_usuario.filter(
            pun_institucion__icontains=institucion)  # Usar __icontains para búsquedas parciales
    if curso:
        puntajes_usuario = puntajes_usuario.filter(pun_curso=curso)

        # Suponiendo que tienes un modelo Materia para listarlas en el dropdown.
    asignaturas = Gen_Asignatura.objects.filter(asi_estado=True)

    context = {
        'segment': 'puntajes',
        'puntajes': puntajes_usuario,
        'asignaturas': asignaturas,
        'redes': redes,
        'contact': contact,
        'success': success
    }
    html_template = loader.get_template('accounts/puntajes.html')
    return HttpResponse(html_template.render(context, request))


@login_required
def enviar_puntajes(request):
    ancho = 100
    if request.method == 'POST':
        # Aquí obtienes los ID de los puntajes seleccionados y el email del profesor
        puntajes_ids = request.POST.getlist('puntaje_id')
        email_profesor = request.POST.get('email_profesor', '')  # Email por defecto o el proporcionado en el formulario

        # Aquí filtras los puntajes seleccionados
        puntajes_seleccionados = (
            Gen_Puntaje.objects.filter(pun_id__in=puntajes_ids)
            .select_related('jue')
            .select_related('tac')
            .select_related('tac__tem')
            .select_related('tac__act')
        )
        # Construimos el encabezado del mensaje con justificación
        encabezado = f"""
        ¡Hola!
        El estudiante {request.user.first_name} {request.user.last_name} ha reenviado su puntuación de los siguientes juegos:
        Institución: {request.user.institucion}
        Curso: {request.user.curso}
        """.rstrip()  # Eliminamos espacios extra al final de cada línea

        # Construimos el mensaje con los puntajes
        mensaje_puntajes = "".join(
            f"Juego: {p.jue.jue_nombre.ljust(20)}    Materia: {p.pun_materia.ljust(20)}    Tema: {p.tac.tem.tem_nombre.ljust(20)}   Actividad: {p.tac.act.act_nombre.ljust(20)}    Puntaje: {str(p.pun_puntaje).ljust(20)}\n".rjust(
                ancho) for p in puntajes_seleccionados)

        # Unimos el encabezado con los puntajes
        mensaje_completo = f"{encabezado}\n{mensaje_puntajes}"
        # Enviar correo electrónico
        send_mail(
            'Puntajes estudiante',
            mensaje_completo,
            'sayala7986@gmail.com',  # El email desde el cual se envía
            [email_profesor],
            fail_silently=False,
        )
        request.session['success'] = True
        return redirect('home:puntajes')
        # Redireccionar a la página deseada después del envío
    return redirect('home:puntajes')

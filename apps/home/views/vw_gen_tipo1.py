
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from apps.gen.models import *
import json
from urllib.parse import unquote
from apps.home.forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

def tipo1(request, tip_id, jue_id):
    respuestas = Gen_Respuesta.objects.filter(jue=jue_id)
    juego = Gen_Juego.objects.get(jue_id=jue_id)
    tema_actividad = Gen_TemaActividad.objects.get(tac_id=juego.tac_id)
    tema = Gen_Tema.objects.get(tem_id=tema_actividad.tem_id)
    correo = User.objects.get(id=tema.aud_uc).email
    tipo_obj = Gen_Tipo.objects.get(tip_id=tip_id)
    tipo_codigo = int(tipo_obj.tip_codigo) if tipo_obj.tip_codigo.isdigit() else None
    multimedia = Gen_Multimedia.objects.filter(jue=jue_id)
    asignatura = Gen_Asignatura.objects.get(asi_id=tema.asi_id).asi_nombre
    # Seleccionar el template correspondiente según el tip_id
    if tipo_codigo == 1:
        template_name = 'Juegos/Tipo1.html'
    elif tipo_codigo == 2:
        template_name = 'Juegos/Tipo2.html'
    elif tipo_codigo == 3:
        template_name = 'Juegos/Tipo3.html'
    elif tipo_codigo == 4:
        template_name = 'Juegos/Tipo4.html'
    else:
        return JsonResponse({'error': f'No hay un template disponible para el tip_id {tipo_codigo}'})
    data = {
        'juego': juego.__dict__,
        'multimedia': list(multimedia.values()),
        'jue_id': jue_id,
        'tip_id': tip_id,
        'respuestas': list(respuestas.values()),
    }

    return render(request, template_name, data)


#


def jugar_todos(request, json_data):
    json_str = unquote(json_data)
    juegos = json.loads(json_str)
    correo = None
    asignatura = None
    puntajes = []
    all_games = []
    msg = ""
    for juego_data in juegos:
        jue_id = juego_data.get('jue_id')
        juego = Gen_Juego.objects.get(jue_id=jue_id)
        all_games.append(juego)
        puntaje = Gen_Juego.objects.filter(jue_id=jue_id).values_list('jue_puntaje', flat=True).first()
        if puntaje is not None:
            puntajes.append(puntaje)
        tema_actividad = Gen_TemaActividad.objects.get(tac_id=juego.tac_id)
        tema = Gen_Tema.objects.get(tem_id=tema_actividad.tem_id)
        correo = User.objects.get(id=tema.aud_uc).email
        asignatura = Gen_Asignatura.objects.get(asi_id=tema.asi_id).asi_nombre
    puntajes_float = [float(p) for p in puntajes]
    success = False
    if request.method == "POST":


        puntajes_recibidos = list(map(int, request.POST.get('puntaje').split('/')))

        # Actualiza los campos en el modelo de usuario
        if request.user.is_authenticated:
            request.user.institucion = request.POST.get('pun_institucion')
            request.user.curso = request.POST.get('pun_curso')
            request.user.save()

        for juego_data, puntaje_individual in zip(juegos, puntajes_recibidos):
            form = PuntajeForm(request.POST)
            if form.is_valid():

                try:
                    jue_id = juego_data.get('jue_id')
                    print(jue_id)
                    juego = Gen_Juego.objects.get(jue_id=jue_id)
                    tema_actividad = Gen_TemaActividad.objects.get(tac_id=juego.tac_id)

                    puntaje = form.save(commit=False)
                    puntaje.jue = juego
                    puntaje.tac = tema_actividad
                    puntaje.pun_puntaje = puntaje_individual
                    puntaje.aud_uc = tema.aud_uc
                    if 'AIGN_ROLID' in request.session and 'AIGN_USERID' in request.session:
                        rol_usuario_actual = request.session['AIGN_ROLID']
                        usuario_actual = request.session['AIGN_USERID']
                        # print('testttt ', rol_usuario_actual)
                        if rol_usuario_actual == 3:
                            puntaje.aud_um = usuario_actual


                    puntaje.save()
                    # msg += f"Juego: {juego.jue_nombre} - Puntaje: {puntaje_individual}\n"
                except (
                Gen_Juego.DoesNotExist, Gen_TemaActividad.DoesNotExist, Gen_Tema.DoesNotExist, User.DoesNotExist,
                Gen_Asignatura.DoesNotExist):
                    # Aquí puedes manejar el error o simplemente continuar
                    continue

                msg = "Puntaje registrado con éxito para todos los juegos válidos."
                success = True
            else:
                print("Se encontraron errores en el formulario")
                print(form.errors)
        if success:  # si los puntajes se guardaron con éxito
            # aquí llamamos a la función para enviar el correo
            send_puntaje_email(request, all_games, puntajes_recibidos, form)
        return redirect('/../100/temas/')
    else:
        form = PuntajeForm()

    total_puntajes = sum(puntajes)
    context = {
        'segment': 'tipos',
        'Juegos': juegos,
        'form': form,
        'msg': msg,
        'correo': correo,
        'asignatura': asignatura,
        'puntajes': puntajes_float,
        'success': success,
        'total_puntajes': total_puntajes
    }
    html_template = loader.get_template('Juegos/Tipos.html')
    return HttpResponse(html_template.render(context, request))



def send_puntaje_email(request, juegos, puntajes, form):
    juegos_nombres = [j.jue_nombre if hasattr(j, 'jue_nombre') else 'Nombre no disponible' for j in juegos]
    puntajes_mensajes = [f"Juego: {nombre} - Puntaje: {puntaje}" for nombre, puntaje in zip(juegos_nombres, puntajes)]
    puntajes_str = "\n".join(puntajes_mensajes)

    # Mensaje para el estudiante
    message_estudiante = f"""
    ¡Hola {request.POST.get('pun_nombre')} {request.POST.get('pun_apellido')}!

    Tu puntaje ha sido registrado con éxito. Aquí están los detalles:

    Fecha: {request.POST.get('pun_fecha')}
    Nombre: {request.POST.get('pun_nombre')}
    Apellido: {request.POST.get('pun_apellido')}
    Institución: {form.cleaned_data['pun_institucion']} 
    Curso: {form.cleaned_data['pun_curso']}
    Materia: {form.cleaned_data['pun_materia']}
    {puntajes_str}
    """
    subject_estudiante = "Notificación de Puntaciones"
    send_mail(subject_estudiante, message_estudiante, 'quichuauda@gmail.com', [request.POST.get('pun_email')])

    # Mensaje para el profesor
    message_profesor = f"""
    ¡Hola!

    El estudiante {request.POST.get('pun_nombre')} {request.POST.get('pun_apellido')} ha registrado su puntuación en los siguientes juegos:
    Fecha: {request.POST.get('pun_fecha')}
    Institución: {form.cleaned_data['pun_institucion']} 
    Curso: {form.cleaned_data['pun_curso']}
    Materia: {form.cleaned_data['pun_materia']}
    {puntajes_str}
    """
    subject_profesor = "Notificación de Puntuación de un Estudiante"
    send_mail(subject_profesor, message_profesor, 'quichuauda@gmail.com', [request.POST.get('pun_emailprofesor')])









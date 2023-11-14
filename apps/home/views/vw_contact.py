
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.sis.models import *
from apps.home.forms import *
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre_apellido = form.cleaned_data['nombre_apellido']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            # Configura el contenido del correo
            message = f"Nombre y Apellido: {nombre_apellido}\nEmail: {email}\nAsunto: {asunto}\nMensaje: {mensaje}"

            # Dirección de correo del destinatario (correo de soporte)
            recipient_email = 'quichuauda@gmail.com'

            # Envía el correo
            send_mail({asunto}, message, email, [recipient_email])

        return redirect('/../100/contact/')
    else:
        form = ContactForm()


    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()

    context = {'segment': 'contact',
               'redes': redes,
               'contact': contact,
               'form': form
               }
    html_template = loader.get_template('home/contact.html')
    return HttpResponse(html_template.render(context, request))


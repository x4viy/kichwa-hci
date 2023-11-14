
import random
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.gen.models import *
from django.http import JsonResponse
# @login_required(login_url="/login/")
from utils.utils import dictfetchall
from apps.sis.models import *
def nosotros(request):
    # Intenta obtener el ID o usa None si no existe el registro
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None

    inf3 = Sis_Informacion.objects.filter(inf_tipo=2).first()
    inf3_id = inf3.inf_id if inf3 else None

    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    nosotros = Sis_Informaciondetalle.objects.filter(inf_id=inf3_id) if inf3_id else Sis_Informaciondetalle.objects.none()

    # context2 = {'random': rand_num}
    context = {'segment': 'nosotros',
               'redes': redes,
               'contact': contact,
               'nosotros': nosotros
               }
    html_template = loader.get_template('home/nosotros.html')
    return HttpResponse(html_template.render(context, request))


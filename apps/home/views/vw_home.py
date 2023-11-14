
import random
from django import template
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.gen.models import *
from apps.sis.models import *
from django.http import JsonResponse
# @login_required(login_url="/login/")
from utils.utils import dictfetchall


def home(request):
    # Intenta obtener el ID o usa None si no existe el registro
    inf = Sis_Informacion.objects.filter(inf_tipo=3).first()
    inf_id = inf.inf_id if inf else None

    inf2 = Sis_Informacion.objects.filter(inf_tipo=5).first()
    inf2_id = inf2.inf_id if inf2 else None

    inf3 = Sis_Informacion.objects.filter(inf_tipo=1).first()
    inf3_id = inf3.inf_id if inf3 else None

    # Usa el ID para obtener más registros o usa un QuerySet vacío
    contact = Sis_Informaciondetalle.objects.filter(inf_id=inf_id) if inf_id else Sis_Informaciondetalle.objects.none()
    redes = Sis_Informaciondetalle.objects.filter(inf_id=inf2_id) if inf2_id else Sis_Informaciondetalle.objects.none()
    inicio = Sis_Informaciondetalle.objects.filter(inf_id=inf3_id) if inf3_id else Sis_Informaciondetalle.objects.none()

    context = {'segment': 'home',
               'redes': redes,
               'contact': contact,
               'inicio': inicio
               }
    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


# def get_temas(_request,cat_id):
#     temas=list(Gen_Tema.objects.filter(asi_id=cat_id,tem_estado=1).values())
#     if (len(temas) > 0):
#         data = {'message': "Success", 'temas': temas}
#     else:
#         data = {'message': "Not Found"}
#
#     return JsonResponse(data)


def get_asi(_request,asi_id):
    temas=list(Gen_Tema.objects.filter(asi_id=asi_id,tem_estado=1).values())
    if (len(temas) > 0):
        data = {'message': "Success", 'temas': temas}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)
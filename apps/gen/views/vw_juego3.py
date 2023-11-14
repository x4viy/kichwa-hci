# Autor: Bryan Amaya
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import Template, Context, RequestContext
from django.template import loader



def Juego3(request):
    context = {'segment': 'juego3'}
    html_template = loader.get_template('../templates/actividad_c/juego3.html')
    return HttpResponse(html_template.render(context, request))
# Autor: Dre
# Fecha: 18/12/2022 00:00
# Descripción: METODOS Y FUNCIONES ESTANDARIZADAS QUE SE USAN CON FRECUENCIA

import json
import socket
import smtplib
import requests
from bunch import Bunch
from django.db import connection
from django.http import HttpResponse
from core.encryption_util import EncryptDES
from vars import rs
from vars.msg import global_formats


def generar_codigo(table_name, codigo, empid):
    with connection.cursor() as cursor:
        cursor.callproc("sis.fn_generarcodigo", [table_name, codigo, empid])
        row = cursor.fetchone()
    return row


# obtiene el nombre de la tabla
def get_table_name(model):
    return model._meta.db_table.replace('"', '')


# obtener id padre en cuentas
def get_obtidpadre(perid, cuecodigov):
    with connection.cursor() as cursor:
        cursor.callproc("con.fn_obtidpadre", [perid, cuecodigov])
        row = cursor.fetchone()
    return row


# Valilda el codigo al momento de actualizar en cuentas
def verifica_codigo_pc(cue_codigov, emp_id, cue_id, cue_grupo, per_id):
    with connection.cursor() as cursor:
        cursor.callproc("con.fn_val_verificacodigopc",
                        [cue_codigov, emp_id, cue_id,
                         cue_grupo, per_id, 6])
        rowData = cursor.fetchall()
        result = []
        for r in rowData:
            result.append(list(r))
        if r[0] != None:
            return result


# clase para imprimir errores en pantalla
class MyException(Exception):
    pass


def recuperarPermisos(session, opc_codigo):
    # Pregunta si tiene el metodo get
    if hasattr(session, 'get'):
        json_values = json.loads(json.dumps(session.get('AIGN_OPCIONES')))
    else:
        json_values = json.loads(json.dumps(session))

    __PERMISOS = []
    for n in json_values:
        if n['opc_codigo'] == opc_codigo:
            __PERMISOS = n
    if not __PERMISOS:
        raise MyException('No existe referencia: ' + opc_codigo + '')
    else:
        return __PERMISOS


# convierte cursor a diccionario de datos
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def ifnull(var, val):
    if var is None or 'None':
        return val
    return var


def get_paramsValues(kwargs):
    params = Bunch()
    format = Bunch()
    if kwargs is not None and 'format' in kwargs:
        try:
            params.update(kwargs)  # parametros
            format.update(kwargs['format'][0])  # decimales
        except:
            format.par_regex = global_formats.format_coin
            format.par_valor = global_formats.decimals_max
    else:
        format.par_regex = global_formats.format_coin
        format.par_valor = global_formats.decimals_max
    return params, format



_e = EncryptDES()


# Metodo que envia correo para notificar la caducidad de FE
def notificar_caducidad_firma(correos, tempo_vigencia):
    # Parametros tempo_vigencia, destinatario
    gmail_user = "erpuda@uazuay.edu.ec"
    app_password = 'erpuda2018'
    sent_from = gmail_user
    to = correos  # ['sebastiantoledo@es.uazuay.edu.ec']
    subject = 'Su firma electronica esta por caducar. Tiempo de vigencia: {}'.format(tempo_vigencia)
    body = 'Su firma electronica esta por caducar. Tiempo de vigencia: {}'.format(tempo_vigencia)
    email_text = 'Subject: {}\n\nReporte de novedades: {}'.format(subject, body)

    # Solicitud de envío de correo
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, app_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Alerta por correo enviada!', tempo_vigencia)
    except Exception as e:
        print(e)
        print('Error en la alerta!')


def get_ip_address():
    '''
    Get the ip address of the running server
    :return: String representing the server's IP address.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


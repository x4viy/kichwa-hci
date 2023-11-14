# Creado por: LG
# Fecha: 29/11/2021
# Objetivo: Variables para las peticiones de los reportes en ReportServer (RS)
from django.db import connection, connections

from utils import utils


class ELEMENTS:
    ID = None  # ID del reporte
    USER = 'root'
    APIKEY = '123456'
    PARAMETROS = {}
    FORMAT = 'pdf'  # CSV PDF EXCEL
    DOWNLOAD = 'False'  # Descarga directa
    IP = '172.16.1.77'  # ip del servidor - probar luego con localhost cuando se suba a produccion
    PORT = '8080'

    def getURL(self):
        try:
            with connections['reportserver'].cursor() as cursor:
                cursor.execute("select r.id, r.key_field, r.name_field, p.name_field ,p.key_field, p.n "
                               "from rs_report r,rs_report_2_param_def rp,rs_parameter_definition p "
                               "where r.id = rp.report_id and rp.parameter_definitions_id = p.entity_id "
                               "and r.name_field = %s order by rp.report_id,p.n ", [self.ID])
                data = utils.dictfetchall(cursor)

                url = 'http://' + self.IP + ':' + self.PORT + '/reportserver/httpauthexport?id=' + str(
                    data[0]['id']) + '&user=' + self.USER + '&apikey=' + self.APIKEY

                for key, value in self.PARAMETROS.items():
                    for row in data:
                        if row['name_field'] == key:
                            url += '&p_' + row['name_field'] + '=' + str(value)

                url += '&format=' + self.FORMAT + '&download=' + self.DOWNLOAD
                return url
        except Exception as e:
            raise Exception('Error al generar reporte: ' + str(e))




class REP_CONTABILIDAD_IDS:
    # reportes y sus keys
    # si se modifica el reporte en reportserver solo debe verificar que siga con el mismo nombre
    REP_CON_ASIENTOSXESTADO_ID = 'REP_CON_ASIENTOSXESTADO'
    REP_CON_ASIENTOCONTABLE_ID = 'REP_CON_ASIENTOCONTABLE'
    REP_CON_TRANSACCIONCABDET_ID = 'REP_CON_TRANSACCIONCABDET'
    REP_CON_MOVIMIENTOCUE_RANGO_ID = 'REP_CON_MOVIMIENTOCUE_RANGO'
    REP_CON_MAYORTRAN_ID = 'REP_CON_MAYORTRAN'
    REP_CON_BALANCE_ID = 'REP_CON_BALANCE'
    REP_CON_BSITUACION_FINANCIERA_ID = 'REP_CON_BSITUACION_FINANCIERA'
    REP_CON_ESTADO_RESUL_ID = 'REP_CON_ESTADO_RESUL'
    REP_CON_FLUJOEFECTIVO_ID = 'REP_CON_FLUJOEFECTIVO'

class REP_VENTAS_IDS:
    REP_GEN_ANTICIPO_ID = 'REP_GENANTICIPO'
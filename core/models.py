from crum import get_current_request
from django.db import models, connection
from django.forms import model_to_dict
from django.utils import timezone

# Clase base para extender funcionalidades
class ERPBaseModel(models.Model):
    usuario_actual = None  # Definir la variable de clase
    # auto_now_add=True => hace que solo se agregue la fecha en de creación y en modificar no cambia
    aud_fc = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # editable=False => hace que ese campo NO permita cambiar su valor en modificación
    aud_uc = models.BigIntegerField(null=True, blank=True, editable=False)
    # auto_now=True => siempre agrega la hora por defecto
    aud_fm = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name="Modificado el")
    aud_um = models.BigIntegerField(null=True, blank=True)
    aud_am = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        abstract = True

    # cambiando el metodo original "save()", para agregar el usuario
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        req = get_current_request()
        # from appls.administracion.models import Adm_Tabla
        # Verificar si el modelo posee auditoría de nivel 2
        # nivel_auditoria = Adm_Tabla.objects.filter(tab_nombre=self.get_table_name()).values('tab_aud_nivel').get()

        # importante: ver comentarios de campos de auditoria, verificar si excluir campos de formularios
        if self.pk is None:
            # self.aud_uc = req.user.pk
            # print('bro el usuario actual es ', self.usuario_actual)
            # rol_usuario_actual = self.request.session['AIGN_ROLID']

            print('ggg', self.aud_uc)


            if self.aud_uc != None:
                self.aud_uc = self.aud_uc
                if self.aud_um != None:
                    self.aud_um = self.aud_um
                else:
                    self.aud_um = self.aud_uc



            else:
                self.aud_uc = 1
                # self.aud_um = req.user.pk
                self.aud_um = 1
            # self.aud_fc = timezone.now()

            print(self.usuario_actual)
            print(self.usuario_actual)
            if self.usuario_actual:
                self.aud_uc = self.usuario_actual
                self.aud_um = self.usuario_actual
            self.aud_am = 'N'
            super().save()
            # if nivel_auditoria['tab_aud_nivel'] == 1:
            # self.callBinnacle('CREAR', req.user.pk, req.user.emp.emp_id)
            self.callBinnacle('CREAR', 1, 1)
        else:
            # self.aud_um = req.user.pk
            self.aud_um = 1
            # self.aud_fc = timezone.now()

            if self.usuario_actual:
                self.aud_um = self.usuario_actual
                # print('qqq ', self.usuario_actual)
            self.aud_am = 'M'
            # if nivel_auditoria['tab_aud_nivel'] == 1:
            # self.callBinnacle('EDITAR', req.user.pk, req.user.emp.emp_id)
            self.callBinnacle('EDITAR', 1, 1)
            super().save()

    # obtiene el nombre de la tabla
    def get_table_name(self):
        return self._meta.db_table.replace('"', '')

    # eliminado lógico
    # def logical_delete(self):
    #     req = get_current_request()
    #     with connection.cursor() as cursor:
    #         cursor.execute("call adm.pr_eliminarregistro(%s, %s, %s);", (self.get_table_name(), self.pk, req.user.pk))
    #     from appls.administracion.models import Adm_Tabla
    #     # Verificar si el modelo posee auditoría de nivel 2
    #     nivel_auditoria = Adm_Tabla.objects.filter(tab_nombre=self.get_table_name()).values('tab_aud_nivel').get()
    #
    #     if nivel_auditoria['tab_aud_nivel'] == 1:
    #         self.callBinnacle('ELIMINAR', req.user.pk, req.user.emp.emp_id)

    # obtener el regostro(s) en formato JSON
    def toJson(self):
        return model_to_dict(self)

        #
        # Función setBinnacle(formulario, operacion, usuario, tabla, empresa, id_registro_value, modelo_actual
        # Autores: Diego Orellana y Jorge Peralta
        #
        # Esta función se encarga de llamar al método de la bitácora.
        #
        # :param self: modelo que se está utilizando.
        # :param operacion: operación que se está realizando.
        # :param usuario: usuario que realiza la acción.
        # :param empresa: empresa a la que pertenece el usuario.
        #
        # :return: Void.
        #

    def callBinnacle(self, operacion, usuario, empresa):
        setBinnacle(self.toJson(), operacion, usuario, self.get_table_name(), empresa, self.pk, self)

# Función setBinnacle(formulario, operacion, usuario, tabla, empresa, id_registro_value, modelo_actual
# Autores: Diego Orellana y Jorge Peralta
#
# Esta función se encarga de registrar en la bitácora la acción realizada por el usuario.
#
# :param formulario: formulario que se está utilizando.
# :param operacion: operación que se está realizando.
# :param usuario: usuario que realiza la acción.
# :param tabla: tabla que se está modificando.
# :param empresa: empresa a la que pertenece el usuario.
# :param id_registro_value: valor del id del registro.
# :param modelo_actual: modelo que se está modificando.
#
# :return: Void.
#
def setBinnacle(formulario, operacion, usuario, tabla, empresa, id_registro_value, modelo_actual):
    campos = formulario
    valor_anterior = ''
    for columna, valor in campos.items():
        if operacion == 'CREAR':
            valor_anterior = None
            saveBinnacle(columna, operacion, valor_anterior, valor, tabla, usuario, empresa, id_registro_value)
        else:
            # pk_column_value = getattr(modelo_actual.objects.get(pk=id_registro_value), columna)
            # pk_column_value = getattr(modelo_actual._class_.objects.get(pk=id_registro_value), columna)
            # if operacion == 'EDITAR':
            #     if pk_column_value != valor:
            #         valor_anterior = pk_column_value
            saveBinnacle(columna, operacion, valor_anterior, valor, tabla, usuario, empresa,
                                 id_registro_value)
                # else:
                #     valor_anterior = None
            # elif operacion == 'ELIMINAR':
            #     valor_anterior = pk_column_value
            #     saveBinnacle(columna, operacion, valor_anterior, None, tabla, usuario, empresa, id_registro_value)


#
# Función saveBinnacle(col, op, val_ant, val_nue, tab, usu, emp)
# Autores: Diego Orellana y Jorge Peralta
#
# Esta función se encarga de registrar en la base de datos la acción realizada por el usuario en la bitácora.
#
# :param col: nombre de la columna.
# :param op: operación que se está realizando.
# :param val_ant: valor anterior de la columna.
# :param val_nue: valor nuevo de la columna.
# :param tab: tabla a la que pertenece la columna.
# :param usu: usuario que realiza la acción.
# :param emp: empresa a la que pertenece el usuario.
#
# :return: Void.
#
def saveBinnacle(col, op, val_ant, val_nue, tab, usu, emp, id_reg):
    # from appls.sesion.models import Adm_Auditoria_N2
    # last_value_aud = Adm_Auditoria_N2.objects.all().aggregate(Max('audn2_id'))
    # if last_value_aud['audn2_id__max'] is None:
    last_value_aud = 1
    # else:
    #     last_value_aud = last_value_aud['audn2_id__max'] + 1

    if "aud_" in col:
        pass
    # else:
    #     Adm_Auditoria_N2.objects.create(
    #         audn2_id=last_value_aud,
    #         audn2_columna=col,
    #         audn2_operacion=op,
    #         audn2_valor_anterior=val_ant,
    #         audn2_valor_nuevo=val_nue,
    #         tab_nombre=tab,
    #         usu_id=usu,
    #         emp_id=emp,
    #         audn2_registro_id=id_reg
    #     )
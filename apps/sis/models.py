from django.db import models
from core.models import ERPBaseModel
from ckeditor.fields import RichTextField
# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de Informacion.


CHOICES_TIPO_INF = [
    (1, 'Inicio'),
    (2, 'Nosotros'),
    (3, 'Contáctanos'),
    (4, 'Términos y condiciones'),
    (5, 'Redes sociales')
]

CHOICES_TIPO_OPC = [
    (1, 'Menú'),
    (2, 'Opción')
]


class Sis_Informacion(ERPBaseModel):
    inf_id = models.BigAutoField(primary_key=True, verbose_name='ID_Informacion')
    inf_nombre = models.CharField(max_length=150, verbose_name='Titulo')
    inf_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name='Descripción')
    inf_tipo = models.SmallIntegerField(choices=CHOICES_TIPO_INF, verbose_name='Sección')
    inf_estado = models.SmallIntegerField(default=1, verbose_name='Estado')

    class Meta:
        managed = False
        verbose_name = 'Información'
        verbose_name_plural = 'Información'
        db_table = 'sis\".\"informacion'

    def __str__(self):
        return self.inf_nombre + ": " + self.inf_descripcion

# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de Informaciondetalle.
class Sis_Informaciondetalle(ERPBaseModel):
    ind_id = models.BigAutoField(primary_key=True, verbose_name="ID_Detalle")
    inf = models.ForeignKey(Sis_Informacion, models.DO_NOTHING, verbose_name="Información")
    ind_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    ind_descripcion = models.CharField(max_length=10000, blank=True, null=True, verbose_name="Descripción (SHIFT+ENTER para saltar linea)")
    ind_estado = models.SmallIntegerField(verbose_name="Estado", default=True)

    class Meta:
        managed = False
        verbose_name = 'informacionetalle'
        verbose_name_plural = 'informaciondetalles'
        db_table = 'sis\".\"informaciondetalle'

    def __str__(self):
        return self.ind_nombre + ": " + self.ind_descripcion

# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de Opcion.
class Sis_Opcion(ERPBaseModel):
    opc_id = models.BigAutoField(primary_key=True, verbose_name="ID_Opcion")
    opc_idpadre = models.ForeignKey('self', models.DO_NOTHING, db_column='opc_idPadre', blank=True, null=True, verbose_name="Padre")  # Field name made lowercase.
    opc_codigov = models.CharField(max_length=10, verbose_name="Código")
    opc_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    opc_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name="Descripción")
    opc_url = models.CharField(max_length=500, verbose_name="URL")
    opc_icono = models.CharField(max_length=150, blank=True, null=True, verbose_name="Icono")
    opc_tipo = models.SmallIntegerField(choices=CHOICES_TIPO_OPC, verbose_name="Tipo")
    opc_orden = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Orden")
    opc_estado = models.SmallIntegerField(default=True)

    class Meta:
        managed = False
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'
        db_table = 'sis\".\"opcion'

    def __str__(self):
        return self.opc_codigov  + ": " + self.opc_nombre

# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de OpcionRol.
class Sis_OpcionRol(ERPBaseModel):
    oro_id = models.BigAutoField(primary_key=True)
    opc = models.ForeignKey(Sis_Opcion, models.DO_NOTHING)
    rol_id = models.BigIntegerField()
    oro_esactivo = models.SmallIntegerField(db_column='oro_esActivo', verbose_name='Activo')  # Field name made lowercase.
    oro_estado = models.SmallIntegerField(default=True)

    class Meta:
        managed = False
        verbose_name = 'Opcion_rol'
        verbose_name_plural = 'Opciones_rol'
        db_table = 'sis\".\"opcion_rol'
        
        
        
class Sis_Rol(ERPBaseModel):
    rol_id = models.BigAutoField(primary_key=True, verbose_name="ID_Rol")
    rol_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre")
    rol_tipo = models.SmallIntegerField(blank=True, null=True, verbose_name="Tipo")
    rol_estado = models.SmallIntegerField(default=True, verbose_name= "Estado")

    class Meta:
        managed = False
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        db_table = 'sis\".\"rol'

    # def __str__(self):
    #     return str(self.rol_id) + ": " + str(self.rol_nombre)

    def __str__(self):
        return self.rol_nombre
    # Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de Usuario.
class Sis_Usuario(ERPBaseModel):
    usu_id = models.BigAutoField(primary_key=True, verbose_name="ID_Usuario")
    usu_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    usu_correo = models.CharField(max_length=100, verbose_name="Correo")
    usu_usuario = models.CharField(max_length=25, blank=True, null=True, verbose_name="Usuario")
    usu_contrasena = models.CharField(max_length=150, blank=True, null=True, verbose_name="Contrasena")
    usu_estado = models.SmallIntegerField(default=True, verbose_name="Estado")
    rol = models.ForeignKey(Sis_Rol, models.DO_NOTHING, verbose_name="Rol")
    class Meta:
        managed = False
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'sis\".\"usuario'

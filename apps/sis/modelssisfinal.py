# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Informacion(models.Model):
    inf_id = models.BigAutoField(primary_key=True)
    inf_nombre = models.CharField(max_length=150)
    inf_descripcion = models.CharField(max_length=500, blank=True, null=True)
    inf_tipo = models.SmallIntegerField()
    inf_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'informacion'


class Informaciondetalle(models.Model):
    ind_id = models.BigAutoField(primary_key=True)
    inf = models.ForeignKey(Informacion, models.DO_NOTHING)
    ind_nombre = models.CharField(max_length=150)
    ind_descripcion = models.CharField(max_length=500, blank=True, null=True)
    ind_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'informacionDetalle'


class Opcion(models.Model):
    opc_id = models.BigAutoField(primary_key=True)
    opc_idpadre = models.ForeignKey('self', models.DO_NOTHING, db_column='opc_idPadre', blank=True, null=True)  # Field name made lowercase.
    opc_codigov = models.CharField(max_length=10)
    opc_nombre = models.CharField(max_length=30)
    opc_descripcion = models.CharField(max_length=60, blank=True, null=True)
    opc_url = models.CharField(max_length=-1)
    opc_icono = models.CharField(max_length=40, blank=True, null=True)
    opc_tipo = models.SmallIntegerField()
    opc_orden = models.DecimalField(max_digits=3, decimal_places=0)
    opc_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'opcion'


class OpcionRol(models.Model):
    oro_id = models.BigAutoField(primary_key=True)
    opc = models.ForeignKey(Opcion, models.DO_NOTHING)
    oro_esactivo = models.SmallIntegerField(db_column='oro_esActivo')  # Field name made lowercase.
    oro_estado = models.SmallIntegerField()
    rol = models.ForeignKey('Rol', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opcion_rol'


class Rol(models.Model):
    rol_id = models.BigAutoField(primary_key=True)
    rol_nombre = models.CharField(max_length=20, blank=True, null=True)
    rol_tipo = models.SmallIntegerField(blank=True, null=True)
    rol_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'rol'


class Usuario(models.Model):
    usu_id = models.BigAutoField(primary_key=True)
    usu_nombre = models.CharField(max_length=150)
    usu_correo = models.CharField(max_length=100)
    usu_usuario = models.CharField(max_length=25)
    usu_contrasena = models.CharField(max_length=-1)
    usu_estado = models.SmallIntegerField()
    rol = models.ForeignKey(Rol, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actividad(models.Model):
    act_id = models.BigAutoField(primary_key=True)
    act_nombre = models.CharField(max_length=50)
    act_descripcion = models.CharField(max_length=500, blank=True, null=True)
    act_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'actividad'


class Asignatura(models.Model):
    asi_id = models.BigAutoField(primary_key=True)
    asi_nombre = models.CharField(max_length=150)
    asi_descripcion = models.CharField(max_length=500, blank=True, null=True)
    asi_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'asignatura'


class Juego(models.Model):
    jue_id = models.BigAutoField(primary_key=True)
    jue_nombre = models.CharField(max_length=50)
    jue_descripcion = models.CharField(max_length=500)
    jue_enunciado = models.CharField(max_length=500, blank=True, null=True)
    jue_puntaje = models.DecimalField(max_digits=3, decimal_places=2)
    jue_estado = models.SmallIntegerField()
    tip = models.ForeignKey('Tipo', models.DO_NOTHING, blank=True, null=True)
    tac = models.ForeignKey('TemaActividad', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juego'


class Multimedia(models.Model):
    mul_id = models.BigAutoField(primary_key=True)
    tem = models.ForeignKey('Tema', models.DO_NOTHING, blank=True, null=True)
    act = models.ForeignKey(Actividad, models.DO_NOTHING, blank=True, null=True)
    res = models.ForeignKey('Respuesta', models.DO_NOTHING, blank=True, null=True)
    jue = models.ForeignKey(Juego, models.DO_NOTHING, blank=True, null=True)
    mul_archivo = models.CharField(max_length=1000)
    mul_tipo = models.CharField(max_length=25)
    mul_formato = models.CharField(max_length=10, blank=True, null=True)
    mul_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'multimedia'


class Puntaje(models.Model):
    pun_id = models.BigAutoField(primary_key=True)
    jue = models.ForeignKey(Juego, models.DO_NOTHING, blank=True, null=True)
    tac = models.ForeignKey('TemaActividad', models.DO_NOTHING, blank=True, null=True)
    pun_nombre = models.CharField(max_length=100, blank=True, null=True)
    pun_apellido = models.CharField(max_length=100, blank=True, null=True)
    pun_institucion = models.CharField(max_length=150, blank=True, null=True)
    pun_curso = models.CharField(max_length=50, blank=True, null=True)
    pun_materia = models.CharField(max_length=50, blank=True, null=True)
    pun_puntaje = models.DecimalField(max_digits=4, decimal_places=2)
    pun_fecha = models.DateField()
    pun_emailprofesor = models.CharField(db_column='pun_emailProfesor', max_length=150, blank=True, null=True)  # Field name made lowercase.
    pun_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'puntaje'


class Respuesta(models.Model):
    res_id = models.BigAutoField(primary_key=True)
    jue = models.ForeignKey(Juego, models.DO_NOTHING)
    res_respuesta = models.CharField(max_length=150)
    res_escorrecta = models.BooleanField()
    res_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'respuesta'


class Tema(models.Model):
    tem_id = models.BigAutoField(primary_key=True)
    asi = models.ForeignKey(Asignatura, models.DO_NOTHING)
    tem_nombre = models.CharField(max_length=150)
    tem_descripcion = models.CharField(max_length=500, blank=True, null=True)
    tem_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tema'


class TemaActividad(models.Model):
    tac_id = models.BigAutoField(primary_key=True)
    act = models.ForeignKey(Actividad, models.DO_NOTHING, blank=True, null=True)
    tem = models.ForeignKey(Tema, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tema_actividad'


class Tipo(models.Model):
    tip_id = models.BigAutoField(primary_key=True)
    tip_codigo = models.CharField(max_length=10)
    tip_nombre = models.CharField(max_length=30)
    tip_descripcion = models.CharField(max_length=30, blank=True, null=True)
    tip_estado = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tipo'

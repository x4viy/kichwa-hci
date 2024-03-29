from django.db import models
from django.utils import timezone
from django.conf import settings
import os

from core.models import ERPBaseModel

# Autor: Dre
# Fecha: 27/12/2022 14:27
# Descripción: Opciones para que puedan sar usadas en una listbox o choices.
CHOICES_TIPO_ACT = [
    (1, 'Seleccione la correcta'),
    (2, 'Arrastrar opciones'),
    (3, 'Escuche y repita'),
    (4, 'Identifique la imagen'),
]


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de categoría.
class Gen_Asignatura(ERPBaseModel):
    asi_id = models.BigAutoField(primary_key=True, verbose_name="Asignatura")
    asi_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    asi_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name="Descripción")
    asi_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        db_table = 'gen\".\"asignatura'

    def __str__(self):
        return str(self.asi_id) + ": " + str(self.asi_nombre)


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de Tema.
class Gen_Tema(ERPBaseModel):
    tem_id = models.BigAutoField(primary_key=True, verbose_name="ID_Tema")
    # usu_id = models.BigIntegerField(verbose_name="ID_Usuario")
    asi = models.ForeignKey(Gen_Asignatura, models.DO_NOTHING, verbose_name="Asignatura")
    tem_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    tem_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name="Descripción")
    # tem_tipo = models.SmallIntegerField(choices=CHOICES_TIPO_ACT, verbose_name="tem_tipo")
    tem_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        db_table = 'gen\".\"tema'

    def __str__(self):
        return str(self.tem_id) + ": " + str(self.tem_nombre)


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de actividad.
class Gen_Actividad(ERPBaseModel):
    act_id = models.BigAutoField(primary_key=True, verbose_name="ID_Actividad")
    # tem = models.ForeignKey(Gen_Tema, models.DO_NOTHING, related_name='fk_tema_actividad', verbose_name="Tema")
    act_nombre = models.CharField(max_length=150, verbose_name="Nombre")
    act_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name="Descripción")
    act_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        db_table = 'gen\".\"actividad'
        # unique_together = (('act_id', 'tem'),)

    # def __str__(self):
    #     return "Tema: "+ str(self.act_id) + ' ' + str(self.tem.tem_nombre) + "- Act: " + str(self.act_nombre)


class Gen_TemaActividad(ERPBaseModel):
    tac_id = models.BigAutoField(primary_key=True, verbose_name='ID')
    act = models.ForeignKey('Gen_Actividad', models.DO_NOTHING, blank=True, null=True, verbose_name='Actividad')
    tem = models.ForeignKey('Gen_Tema', models.DO_NOTHING, blank=True, null=True, verbose_name='Tema')
    tac_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Tac'
        verbose_name_plural = 'Tacs'
        db_table = 'gen\".\"tema_actividad'

    def __str__(self):
        if self.pk is None:  # Nuevo registro sin guardar
            return 'Nuevo Gen_TemaActividad'
        else:
            act_nombre = self.act.act_nombre if self.act else 'Sin nombre de actividad'
            tem_nombre = self.tem.tem_nombre if self.tem else 'Sin nombre de tema'
            return f"{tem_nombre}: {act_nombre}"


class Gen_Tipo(ERPBaseModel):
    tip_id = models.BigAutoField(primary_key=True, verbose_name='ID_Tipo')
    tip_codigo = models.CharField(max_length=10, verbose_name='Codigo')
    tip_nombre = models.CharField(max_length=150, verbose_name='Nombre')
    tip_descripcion = models.CharField(max_length=500, blank=True, null=True, verbose_name='Descripción')
    # tip_icono = models.CharField(max_length=150, blank=True, null=True, verbose_name="Icono")
    tip_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        db_table = 'gen\".\"tipo'

    def __str__(self):
        return str(self.tip_codigo) + ": " + str(self.tip_nombre)


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de juego.
class Gen_Juego(ERPBaseModel):
    jue_id = models.BigAutoField(primary_key=True, verbose_name='ID_Juego')
    tip = models.ForeignKey('Gen_Tipo', models.DO_NOTHING, blank=True, null=True, verbose_name='Tipo')
    tac = models.ForeignKey('Gen_TemaActividad', models.DO_NOTHING, blank=True, null=True,
                            verbose_name='Tema: actividad')
    jue_nombre = models.CharField(max_length=150, verbose_name='Nombre')
    jue_descripcion = models.CharField(max_length=500, verbose_name='Descripción')
    jue_enunciado = models.CharField(max_length=500, blank=True, null=True, verbose_name='Enunciado')
    jue_puntaje = models.DecimalField(max_digits=7, decimal_places=3, verbose_name='Puntaje', default=1)
    jue_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        db_table = 'gen\".\"juego'
    # def __str__(self):
    #     return str(self.act.act_id) + ": " + str(self.act.act_nombre)


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    print('rename')
    print('IMPORTTANTE ', filename)
    fecha_hora_actual = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = '{}.{}'.format(fecha_hora_actual, ext)
    return filename


def convertir_a_minusculas(texto):
    return texto.lower()


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de multimedia.
class Gen_Multimedia(ERPBaseModel):
    mul_id = models.BigAutoField(primary_key=True, verbose_name='ID_Multimedia')
    tem = models.ForeignKey('Gen_Tema', models.DO_NOTHING, blank=True, null=True, verbose_name='Tema')
    act = models.ForeignKey('Gen_Actividad', models.DO_NOTHING, blank=True, null=True, verbose_name='Actividad')
    res = models.ForeignKey('Gen_Respuesta', models.DO_NOTHING, blank=True, null=True, verbose_name='Respuesta')
    jue = models.ForeignKey('Gen_Juego', models.DO_NOTHING, blank=True, null=True, verbose_name='Juego')
    tip = models.ForeignKey('Gen_Tipo', models.DO_NOTHING, blank=True, null=True, verbose_name='Tipo')
    # mul_archivo = models.BinaryField()
    # mul_archivo = models.FileField(upload_to='', verbose_name='Archivo')
    mul_archivo = models.FileField(upload_to=path_and_rename, verbose_name='Multimedia')
    mul_tipo = models.CharField(max_length=25, verbose_name='Tipo')
    mul_formato = models.CharField(max_length=10, blank=True, null=True, verbose_name='Formato')
    mul_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.mul_archivo)
        filename = self.mul_archivo.name
        if not filename.startswith(settings.MEDIA_URL):
            filename = f'{settings.MEDIA_URL}{filename}'
        self.mul_archivo.name = filename
        if self.mul_formato:
            print(self.mul_formato)
            self.mul_formato = convertir_a_minusculas(self.mul_formato)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = 'Multimedia'
        verbose_name_plural = 'Multimedias'
        db_table = 'gen\".\"multimedia'
        unique_together = (('mul_id'),)


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de puntaje.
class Gen_Puntaje(ERPBaseModel):
    pun_id = models.BigAutoField(primary_key=True, verbose_name="ID_Puntaje")
    jue = models.ForeignKey('Gen_Juego', models.DO_NOTHING, blank=True, null=True)
    tac = models.ForeignKey('Gen_TemaActividad', models.DO_NOTHING, blank=True, null=True)
    pun_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre")
    pun_apellido = models.CharField(max_length=150, blank=True, null=True, verbose_name="Apellido")
    pun_institucion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Institucion")
    pun_curso = models.CharField(max_length=150, blank=True, null=True, verbose_name="Curso")
    pun_materia = models.CharField(max_length=150, blank=True, null=True, verbose_name="Materia")
    pun_puntaje = models.DecimalField(max_digits=7, decimal_places=3, verbose_name="Puntaje")
    pun_fecha = models.DateField(verbose_name="Fecha")
    pun_email = models.CharField(db_column='pun_email', max_length=150, blank=True, null=True, verbose_name="Correo del estudiante")  # Field name made lowercase.
    pun_emailprofesor = models.CharField(db_column='pun_emailprofesor', max_length=150, blank=True, null=True, verbose_name="Correo del profesor")  # Field name made lowercase.
    pun_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Puntaje'
        verbose_name_plural = 'Puntajes'
        db_table = 'gen\".\"puntaje'


# Autor: Bryan Amaya
# Fecha: 09/05/2023 09:00
# Descripción: Modelo de respuesta.
class Gen_Respuesta(ERPBaseModel):
    res_id = models.BigAutoField(primary_key=True, verbose_name="ID_Respuesta")
    jue = models.ForeignKey(Gen_Juego, models.DO_NOTHING, blank=True, null=True, verbose_name='Juego')
    res_respuesta = models.CharField(max_length=150, verbose_name="Respuesta")
    res_escorrecta = models.BooleanField(db_column='res_escorrecta',
                                         verbose_name="Respuesta Correcta")  # Field name made lowercase.
    res_estado = models.SmallIntegerField(default=True, verbose_name="Estado")

    class Meta:
        managed = False
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        db_table = 'gen\".\"respuesta'

    def __str__(self):
        return str(self.res_id) + ": " + str(self.res_respuesta)

# Generated by Django 3.2.16 on 2024-01-04 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sis_Informacion',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('inf_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID_Informacion')),
                ('inf_nombre', models.CharField(max_length=150, verbose_name='Titulo')),
                ('inf_descripcion', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('inf_tipo', models.SmallIntegerField(choices=[(1, 'Inicio'), (2, 'Nosotros'), (3, 'Contáctanos'), (4, 'Términos y condiciones'), (5, 'Redes sociales')], verbose_name='Sección')),
                ('inf_estado', models.SmallIntegerField(default=1, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Información',
                'verbose_name_plural': 'Información',
                'db_table': 'sis"."informacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sis_Informaciondetalle',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('ind_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID_Detalle')),
                ('ind_nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('ind_descripcion', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Descripción (SHIFT+ENTER para saltar linea)')),
                ('ind_estado', models.SmallIntegerField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'informacionetalle',
                'verbose_name_plural': 'informaciondetalles',
                'db_table': 'sis"."informaciondetalle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sis_Opcion',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('opc_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID_Opcion')),
                ('opc_codigov', models.CharField(max_length=10, verbose_name='Código')),
                ('opc_nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('opc_descripcion', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('opc_url', models.CharField(max_length=500, verbose_name='URL')),
                ('opc_icono', models.CharField(blank=True, max_length=150, null=True, verbose_name='Icono')),
                ('opc_tipo', models.SmallIntegerField(choices=[(1, 'Menú'), (2, 'Opción')], verbose_name='Tipo')),
                ('opc_orden', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='Orden')),
                ('opc_estado', models.SmallIntegerField(default=True)),
            ],
            options={
                'verbose_name': 'Opcion',
                'verbose_name_plural': 'Opciones',
                'db_table': 'sis"."opcion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sis_OpcionRol',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('oro_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rol_id', models.BigIntegerField()),
                ('oro_esactivo', models.SmallIntegerField(db_column='oro_esActivo', verbose_name='Activo')),
                ('oro_estado', models.SmallIntegerField(default=True)),
            ],
            options={
                'verbose_name': 'Opcion_rol',
                'verbose_name_plural': 'Opciones_rol',
                'db_table': 'sis"."opcion_rol',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sis_Rol',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('rol_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID_Rol')),
                ('rol_nombre', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre')),
                ('rol_tipo', models.SmallIntegerField(blank=True, null=True, verbose_name='Tipo')),
                ('rol_estado', models.SmallIntegerField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'sis"."rol',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sis_Usuario',
            fields=[
                ('aud_fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('aud_uc', models.BigIntegerField(blank=True, editable=False, null=True)),
                ('aud_fm', models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')),
                ('aud_um', models.BigIntegerField(blank=True, null=True)),
                ('aud_am', models.CharField(blank=True, max_length=1, null=True)),
                ('usu_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID_Usuario')),
                ('usu_nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('usu_correo', models.CharField(max_length=100, verbose_name='Correo')),
                ('usu_usuario', models.CharField(blank=True, max_length=25, null=True, verbose_name='Usuario')),
                ('usu_contrasena', models.CharField(blank=True, max_length=150, null=True, verbose_name='Contrasena')),
                ('usu_estado', models.SmallIntegerField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'sis"."usuario',
                'managed': False,
            },
        ),
    ]
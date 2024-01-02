# Autor: Dre
# Fecha: 18/12/2022 13:00
# Descripción: Aqui se almacenarán todos los elementos para hacer los CRUDs como:
#               - Formularios
#               - Grids (usando la libreria syncfunsion) para cuando se requiera cabecera-detalle
#               - Choices para generar datos estandarizados

from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django.forms import *
from apps.gen.models import *
from core.crispy_layouts import DivHeaderWithButtons, DivGridHeaderWithButtons
from vars.css import Form_CSS
from vars.js import SyncFusionGridOptions
from django.forms.widgets import *
from django.utils.html import mark_safe
from django.db import connection
from utils.utils import dictfetchall
import html
from django.utils.html import format_html
from vars.msg import CRUD_MSG
import string
from contextlib import contextmanager
import sys

@contextmanager
def suppress_console_errors():
    original_stderr = sys.stderr
    sys.stderr = open('NUL', 'w')  # Redirige los errores a un archivo ficticio
    yield
    sys.stderr = original_stderr

# *** Grids *** #


def get_genTemaActividadDetsForm(tem_id):
    # mul_id = CharField(label="mul_id", widget=HiddenInput())
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions()
    opts.grid_id = 'temaactividad_grid'
    opts.grid_title = 'TemaActividad'
    # DropdownList para poner en una celda de la grid

    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]
    # DropdownList para poner en una celda de la grid
    lov_act = list(Gen_Actividad.objects.filter(act_estado=1).values("act_id", "act_nombre"))
    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            'isPrimaryKey': True,
            'editable': False,
            'width': 100,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'tac_id',
            'visible': False,
            'width': 100,
        },
        {'field': 'act_id',
         'headerText': 'actividad',
         'headerName': 'actividad',
         'dataSource': lov_act,
         'foreignKeyField': 'act_id',
         'foreignKeyValue': 'act_nombre',  # MOSTRAR USUARIO,
         'validationRules': {'required': True}
         },
        {
            'field': '_action',
            'visible': True,
            'width': 1,
            'edit': {'params': {'value': 'N'}},
            'defaultValue': 'N',
        }
    ]
    opts.gridOptions['toolbarClick'] = 'toolbarClick'
    opts.gridOptions['rowDataBound'] = 'rowDataBound'
    if True:
        # data = Sis_Rol.objects.filter(rol_id=rol_id, rol_estado=1).only("rol_nombre")
        data = Gen_TemaActividad.objects.filter(tem_id=tem_id, tac_estado=1).only("tac_id",
                                                                                  "act_id",
                                                                                  # "oro_esactivo"
                                                                                  )
        data_list = []
        cont = 1
        for row in data:
            l_row_dict = row.__dict__
            del l_row_dict['_state']
            l_row_dict['_action'] = None
            l_row_dict['id'] = cont
            cont = cont + 1
            data_list.append(l_row_dict)
        opts.gridOptions['dataSource'] = data_list
        # print('opc_id tabla Gen_Act : ', tem_id)
        # print(data_list)
    else:
        opts.gridOptions['dataSource'] = []
    return opts



# Autor: Dre
# Fecha: 17/12/2022 11:00
# Descripción: Grids para Respuestas de la opcion Actividad..
ContadorControl = 0

def get_genRespuestaDetsForm(jue_id):
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions(allowEdit=False)
    opts.grid_id = 'respuesta_grid'
    opts.grid_title = 'Respuesta'
    vista_previa = CharField(label="Vista previa", required=False)

    # DropdownList para poner en una celda de la grid
    # print('hola buenas tardes')
    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]
    opts.gridOptions['toolbar'] = ['Add', 'Edit', 'Delete', 'Update', 'Cancel']
    # opts.gridOptions['toolbarText'] = {
    #     Add: 'Añadir',
    #     edit: 'Editar',
    #     delete: 'Eliminar',
    #     update: 'Actualizar',
    #     cancel: 'Cancelar'
    # }

    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            # 'visible': True,
            # 'width': 100,
            'isPrimaryKey': True,
            'editable': False,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'res_id',
            'visible': True,
            'width': 1,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'mul_id',
            'visible': True,
            'width': 1,
        },
        {
            'field': 'res_respuesta',
            'headerText': Gen_Respuesta._meta.get_field('res_respuesta').verbose_name,
            'headerName': Gen_Respuesta._meta.get_field('res_respuesta').verbose_name,
            'placeholder': 'Nada',
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 100,
        },
        {
            'field': 'res_escorrecta',
            'headerText': Gen_Respuesta._meta.get_field('res_escorrecta').verbose_name,
            'headerName': Gen_Respuesta._meta.get_field('res_escorrecta').verbose_name,
            'sortable': True,
            'filter': True,
            'textAlign': 'Center',
            'allowEditing': True,
            'editType': "booleanedit",
            'type': 'boolean',
            'dataSource': lov_yes_no,
            'foreignKeyField': 'id',
            'foreignKeyValue': 'name',
            'displayAsCheckBox': False,
            'width': 50,
        },
        {
            'field': 'mul_archivo',
            'isPrimaryKey': True,
            'headerText': Gen_Multimedia._meta.get_field('mul_archivo').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('mul_archivo').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': False},
            'width': 100,

            'edit': {
                'create': 'crear',
                'read': 'leer',
                'destroy': 'destruir',
                'write': 'escribir'
            },
        },
        {
            'field': 'mul_tipo',
            'headerText': Gen_Multimedia._meta.get_field('mul_tipo').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('mul_tipo').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 1,

            'edit': {
                'create': 'creardos',
                'read': 'leerdos',
                'destroy': 'destruirdos',
                'write': 'escribirdos'
            },
        },
        {
            'field': 'mul_formato',
            'headerText': Gen_Multimedia._meta.get_field('mul_formato').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('mul_formato').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 1,

            'edit': {
                'create': 'creartres',
                'read': 'leertres',
                'destroy': 'destruirtres',
                'write': 'escribirtres'
            },

        },
        {
            'field': 'vista_previa',
            'headerText': 'Vista Previa',
            'headerName': 'Vista Previa',
            'width': 100,
            'visible': False,
            # 'template': '<h1>${arch}</h1>',
        },
        {
            'field': '_action',
            'visible': True,
            'width': 1,
            'edit': {'params': {'value': 'N'}},
            'defaultValue': 'N',
        }
    ]
    opts.gridOptions['toolbarClick'] = 'toolbarClick'
    opts.gridOptions['rowDataBound'] = 'rowDataBound'

    def validate_res_escorrecta(data):
        true_count = sum(1 for item in data if item['res_escorrecta'])
        if true_count > 1:
            # print('que fue men')
            raise ValidationError("Solo puede haber una respuesta correcta.")

    if True:

        # data = Gen_Respuesta.objects.filter(jue_id=jue_id, res_estado=1).order_by('res_id').only("res_id",
        #                                                                                          "res_respuesta",
        #                                                                                          "res_escorrecta")
        #
        # Gen_Multimedia.objects.filter(jue_id=jue_id, mul_estado=1).order_by('mul_id').only("mul_id",
        #                                                                                          "mul_archivo",
        #                                                                                          "mul_tipo",
        #                                                                                          "mul_formato")
        global ContadorControl
        ContadorControl = ContadorControl + 1
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT res.res_id, res.res_respuesta, res.res_escorrecta, 
                       mul.mul_id, mul.mul_archivo, mul.mul_tipo, mul.mul_formato, null vista_previa
                FROM gen.respuesta AS res
                LEFT JOIN gen.multimedia AS mul ON res.res_id = mul.res_id AND res.jue_id = mul.jue_id
                WHERE res.jue_id = %s AND res.res_estado = 1
                ORDER BY res.res_id, mul.mul_id""",
                           [jue_id])
            data = dictfetchall(cursor)

        # print('data ', jue_id, ContadorControl , data)


        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT mul.mul_id, mul.mul_archivo, mul.mul_tipo, mul.mul_formato, null vista_previa
                FROM gen.multimedia AS mul
                WHERE mul.jue_id = %s"""
                           , [jue_id])
            data2 = dictfetchall(cursor)

        # print('data2 ', jue_id, data2)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT res.res_id, res.res_respuesta, res.res_escorrecta
                FROM gen.respuesta AS res
                WHERE res.jue_id = %s"""
                           , [jue_id])
            data3 = dictfetchall(cursor)

        data_list = []
        cont = 1

        # if not data2 and ContadorControl == 2:
        #     print('Funciono, no hay multimedia')
        #     ContadorControl = 0
        #     for row in data3:
        #         l_row_dict = row
        #         l_row_dict['_action'] = None
        #         l_row_dict['id'] = cont
        #         cont = cont + 1
        #         data_list.append(l_row_dict)
        # elif data2 and ContadorControl == 2:
        #     print('Funciono, hay multimedia')
        #     ContadorControl = 0
        #     for row in data:
        #         l_row_dict = row
        #         l_row_dict['_action'] = None
        #         l_row_dict['id'] = cont
        #         cont = cont + 1
        #         data_list.append(l_row_dict)

        cont1 = 1
        # arch = '<img src="/media/2023-06-09_14-28-49.gif" alt="Vista previa de la imagen" width="100">'
        # arch = '<h1>test2</h1>'
        # for row in data:
        #     l_row_dict = row
        #     arch = l_row_dict['mul_archivo']
        #
        #     # for column in opts.gridOptions['columns']:
        #     #     if column['field'] == 'vista_previa':
        #     # template = string.Template('<h1>$value</h1>')
        #     # l_row_dict['template'] = template.substitute(value=cont1)
        #     # cont1 += 1
        #     #
        #     l_row_dict['vista_previa'] = mark_safe(f'<h1>{cont}</h1>')
        #     l_row_dict['id'] = cont
        #     cont += 1
        #     data_list.append(l_row_dict)
        # # cont = 1
        # # for row in (data2):
        # #     l_row_dict = row.__dict__
        # #     del l_row_dict['_state']
        # #     l_row_dict['_action'] = None
        # #     l_row_dict['id'] = cont
        # #     cont = cont + 1
        # #     print(l_row_dict)
        # #     print('ARRIBA')
        # #     data_list2.append(l_row_dict)
        for row in data:
            l_row_dict = row
            l_row_dict['_action'] = None
            l_row_dict['id'] = cont
            cont = cont + 1
            data_list.append(l_row_dict)
        validate_res_escorrecta(data_list)
        opts.gridOptions['dataSource'] = data_list
        # opts.gridOptions['dataSource'] = data_list2

        # print('act_id tabla Respuesta : ', jue_id)
        # print(data_list)
        # print(data_list2)
    else:
        opts.gridOptions['dataSource'] = []
    return opts


def get_genMultimediaDetsForm(act_id):
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions()
    opts.grid_id = 'multimedia_grid'
    opts.grid_title = 'Multimedia'
    # DropdownList para poner en una celda de la grid

    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]

    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            # 'isPrimaryKey': True,
            'editable': False,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'mul_id',
            'visible': True,
            'width': 1,
        },
        {
            'field': 'mul_archivo',
            'isPrimaryKey': True,
            'headerText': Gen_Multimedia._meta.get_field('mul_archivo').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('mul_archivo').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 100,

            'edit': {
                'create': 'crear',
                'read': 'leer',
                'destroy': 'destruir',
                'write': 'escribir'
            },
        },
        {
            'field': 'mul_tipo',
            'headerText': Gen_Multimedia._meta.get_field('mul_tipo').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('mul_tipo').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 100,

            'edit': {
                'create': 'creardos',
                'read': 'leerdos',
                'destroy': 'destruirdos',
                'write': 'escribirdos'
            },
        },
        {
            'field': '_action',
            'visible': True,
            'width': 1,
            'edit': {'params': {'value': 'N'}},
            'defaultValue': 'N',
        }
    ]
    opts.gridOptions['toolbarClick'] = 'toolbarClick'
    opts.gridOptions['rowDataBound'] = 'rowDataBound'
    # Add this line to add the event listener
    opts.gridOptions['toolbarClick'] = 'handleDeleteButtonClick'
    if True:
        data = Gen_Multimedia.objects.filter(act_id=act_id, mul_estado=1).only("mul_id",
                                                                               "mul_archivo",
                                                                               "mul_tipo")
        data_list = []
        for row in data:
            l_row_dict = row.__dict__
            del l_row_dict['_state']
            l_row_dict['_action'] = None
            data_list.append(l_row_dict)
        opts.gridOptions['dataSource'] = data_list

    else:
        opts.gridOptions['dataSource'] = []
    return opts


# *** FORMULARIOS *** #


# Autor: Bryan Amaya
# Fecha: 10/05/2023
# Descripción: Formulario para la opción 'Multimedia'.
class Gen_MultimediaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Gen_MultimediaForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['tem'].required = True
        self.fields['act'].required = False
        self.fields['res'].required = False
        self.fields['mul_archivo'].required = False
        self.fields['mul_tipo'].required = False
        self.fields['mul_formato'].required = False
        self.fields['tem'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = Form_CSS.fields_label_class
        self.helper.field_class = Form_CSS.fields_field_class
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div('tem',
                    'act',
                    'res',
                    'mul_archivo',
                    'mul_tipo',
                    'mul_formato',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    class Meta:
        model = Gen_Multimedia
        fields = '__all__'
        exclude = ['mul_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Bryan Amaya
# Fecha: 31/05/2023
# Descripción: Formulario para la opción 'Asignatura'.
class Gen_AsignaturaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Gen_AsignaturaForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['asi_nombre'].required = True
        self.fields['asi_descripcion'].required = False
        self.fields['asi_nombre'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = Form_CSS.fields_label_class
        self.helper.field_class = Form_CSS.fields_field_class
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div('asi_nombre',
                    'asi_descripcion',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    class Meta:
        model = Gen_Asignatura
        fields = '__all__'
        exclude = ['asi_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Bryan Amaya
# Fecha: 31/05/2023
# Descripción: Formulario para la opción 'Asignatura'.
class Gen_TipoForm(ModelForm):
    mul_id = CharField(label="ID_Multimedia", widget=HiddenInput())
    mul_archivo = FileField(label="Imagen")
    vista_previa = CharField(label="Vista previa", required=False)
    def __init__(self, *args, **kwargs):
        super(Gen_TipoForm, self).__init__(*args, **kwargs)
        mul_archivo = self.initial.get('mul_archivo')
        # print('enproceso ', mul_archivo)
        if mul_archivo:
            self.fields['vista_previa'].widget = ImagePreviewWidget()
            # print('avanzas', mul_archivo.url)
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            self.fields['vista_previa'].initial = mark_safe(f'{mul_archivo}')
        else:
            self.fields['vista_previa'].widget = HiddenInput()
            self.fields['vista_previa'].initial = ''
        # Cambiar atributos especificos
        self.fields['tip_codigo'].required = True
        self.fields['tip_nombre'].required = True
        self.fields['tip_descripcion'].required = False
        self.fields['mul_id'].required = False
        # self.fields['mul_id'].visible = False
        # self.fields['mul_id'].visible = True
        self.fields['mul_archivo'].required = False
        # self.fields['tip_icono'].required = False
        self.fields['tip_codigo'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = Form_CSS.fields_label_class
        self.helper.field_class = Form_CSS.fields_field_class
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div('tip_codigo',
                    'tip_nombre',
                    'tip_descripcion',
                    'mul_id',
                    'mul_archivo',
                    'vista_previa',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    class Meta:
        model = Gen_Tipo
        fields = '__all__'
        exclude = ['tip_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Bryan Amaya
# Fecha: 06/05/2023
# Descripción: Formulario para la opción 'Juego'.
class Gen_JuegoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Gen_JuegoForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        rol_usuario_actual = self.initial.get('rol_id')
        usuario_actual = self.initial.get('usuario_id')
        self.fields['tac'].required = True
        if rol_usuario_actual != 1:
            self.fields['tac'].queryset = Gen_TemaActividad.objects.filter(aud_uc=usuario_actual)
        else:
            self.fields['tac'].queryset = Gen_TemaActividad.objects.all()
        self.fields['tip'].required = True
        self.fields['jue_nombre'].required = True
        self.fields['jue_descripcion'].required = True
        self.fields['jue_enunciado'].required = True
        self.fields['jue_puntaje'].required = True
        self.fields['jue_nombre'].widget.attrs['autofocus'] = True

        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label  # .lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = 'col-sm-4 text-right form-control-sm'
        self.helper.field_class = 'col-sm-5'
        print('pk ',self.instance.pk)
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('jue_nombre',
                            'jue_descripcion',
                            'tip',
                            css_class='col-sm'
                            ),
                        Div('tac',
                            'jue_enunciado',
                            'jue_puntaje',
                            css_class='col-sm', id='transferencia_id'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ),
            Div(
                TabHolder(
                    Tab(
                        'Respuestas',
                        DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                                                 grid_opts=get_genRespuestaDetsForm(None)),
                    ),
                    # Tab(
                    #     'Multimedia',
                    #     DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                    #                              grid_opts=get_genMultimediaDetsForm(None)),
                    # ),

                ),
            )
        )

    def clean_jue_puntaje(self):
        jue_puntaje = self.cleaned_data['jue_puntaje']

        try:
            jue_puntaje_int = jue_puntaje
            if jue_puntaje_int < 0 or jue_puntaje_int > 1000:
                raise forms.ValidationError("Ingrese un número entre 0 y 1000.")
        except ValueError:
            raise forms.ValidationError("Ingrese un número válido.")

        return jue_puntaje_int

    class Meta:
        model = Gen_Juego
        fields = '__all__'
        exclude = ['jue_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


class Gen_PuntajeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Gen_PuntajeForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['pun_nombre'].required = False
        self.fields['pun_apellido'].required = False
        self.fields['pun_institucion'].required = False
        self.fields['pun_fecha'].required = False
        self.fields['pun_email'].required = False
        self.fields['pun_emailprofesor'].required = False
        self.fields['pun_curso'].required = False
        self.fields['pun_materia'].required = False
        self.fields['pun_puntaje'].required = True
        self.fields['pun_nombre'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = 'col-sm-4 text-right form-control-sm'
        self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Div(
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('pun_fecha', css_class='col-sm-6 mb-4'),  # Fecha
                        Div('pun_emailprofesor',css_class='col-sm-6 mb-4'),  # Espacio en blanco
                        Div('pun_nombre', 'pun_apellido', 'pun_email', css_class='col-sm-6 mb-4'),  # Nombre e Institución
                        Div('pun_institucion', 'pun_curso', 'pun_materia', css_class='col-sm-6 mb-4'),  # Apellido y Curso
                        Div('tac', css_class='col-sm-6 mb-4'),  # Edad
                        Div('pun_puntaje', css_class='col-sm-6 mb-4'),  # Puntaje
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            )
        )
    class Meta:
        model = Gen_Puntaje
        fields = '__all__'
        exclude = ['pun_estado']
        widgets = {}

    def clean(self):
        # super(Gen_PuntajeForm, self).clean()
        form_data = self.cleaned_data
        return form_data


class Gen_RespuestaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Gen_RespuestaForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['act'].required = True
        self.fields['tem_id'].required = True
        self.fields['res_respuesta'].required = True
        self.fields['res_escorrecta'].required = True
        self.fields['act'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = Form_CSS.fields_label_class
        self.helper.field_class = Form_CSS.fields_field_class
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div('act',
                    'tem_id',
                    'res_respuesta',
                    'res_escorrecta',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    class Meta:
        model = Gen_Respuesta
        fields = '__all__'
        exclude = ['res_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Dre
# Fecha: 27/12/2022 14:25
# Descripción: Formulario para la opción 'Actividad'.
class Gen_ActividadForm(ModelForm):
    mul_id = CharField(label="ID_Multimedia", widget=HiddenInput())
    mul_archivo = FileField(label="Imagen")
    vista_previa = CharField(label="Vista previa", required=False)
    # mul_id = CharField(label="mul_id", widget=HiddenInput())
    # mul_archivo = FileField(label="mul_archivo")
    # vista_previa = CharField(label="Vista previa", required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    # vista_previa = CharField(label="Vista previa")


    def __init__(self, *args, **kwargs):
        super(Gen_ActividadForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        # mul_archivo_existe = self.initial.get('mul_archivo_existente')
        mul_archivo = self.initial.get('mul_archivo')
        # print('enproceso ', mul_archivo)
        if mul_archivo:
            self.fields['vista_previa'].widget = ImagePreviewWidget()
            # print('avanzas', mul_archivo.url)
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            self.fields['vista_previa'].initial = mark_safe(f'{mul_archivo}')
        else:
            self.fields['vista_previa'].widget = HiddenInput()
            self.fields['vista_previa'].initial = ''
        # Cambiar a tributos especificos
        # multimedia = Gen_MultimediaForm()
        # print(multimedia)
        # self.fields['usu_id'].required = True
        # self.fields['a'].required = True
        self.fields['act_nombre'].required = True
        self.fields['act_descripcion'].required = False
        self.fields['mul_id'].required = False
        # self.fields['mul_id'].visible = False
        # self.fields['mul_id'].visible = True
        self.fields['mul_archivo'].required = False
        # self.fields['tem_tipo'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label  # .lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = 'col-sm-4 text-right form-control-sm'
        self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('act_nombre',
                            'act_descripcion',
                            'mul_archivo',
                            'mul_id',
                            css_class='col-sm'
                            ),
                        Div('vista_previa',
                            css_class='col-sm', id='transferencia_id'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ),
        )

    class Meta:
        model = Gen_Actividad
        fields = '__all__'
        exclude = ['act_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


class ImagePreviewWidget(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            # print('AYAYAYAYAY ', value)
            return mark_safe(f'<img src={value} alt="Vista previa de la imagen" style="max-width: 150%; max-height: 275px;">')
            # return mark_safe('<h1>teszt</h1>')
        return super().render(name, value, attrs, renderer)


class Gen_TemaForm(ModelForm):
    mul_id = CharField(label="ID_Multimedia", widget=HiddenInput())
    # mul_id = CharField(label="mul_id", widget=HiddenInput())
    # mul_archivo = FileField(label="mul_archivo")
    mul_archivo = FileField(label="Imagen")
    # vista_previa = CharField(label="Vista previa", required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    # vista_previa = CharField(label="Vista previa")
    vista_previa = CharField(label="Vista previa", required=False)

    def __init__(self, *args, **kwargs):
        super(Gen_TemaForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        # mul_archivo_existe = self.initial.get('mul_archivo_existente')
        mul_archivo = self.initial.get('mul_archivo')
        # print('enproceso ', mul_archivo)
        if mul_archivo:
            self.fields['vista_previa'].widget = ImagePreviewWidget()
            # print('avanzas', mul_archivo.url)
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            self.fields['vista_previa'].initial = mark_safe(f'{mul_archivo}')
        else:
            self.fields['vista_previa'].widget = HiddenInput()
            self.fields['vista_previa'].initial = ''
        # Cambiar a tributos especificos
        # multimedia = Gen_MultimediaForm()
        # print(multimedia)
        # self.fields['usu_id'].required = True
        self.fields['asi'].required = True
        self.fields['tem_nombre'].required = True
        self.fields['tem_descripcion'].required = False
        self.fields['mul_id'].required = False
        # self.fields['mul_id'].visible = False
        # self.fields['mul_id'].visible = True
        self.fields['mul_archivo'].required = False
        # self.fields['tem_tipo'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label  # .lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        # self.helper.label_class = Form_CSS.fields_label_class
        # self.helper.field_class = Form_CSS.fields_field_class
        self.helper.label_class = 'col-sm-4 text-right form-control-sm'
        self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Div(
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('tem_nombre',
                            'tem_descripcion',
                            'asi',
                            'mul_id',
                            css_class='col-sm'
                            ),
                        Div('mul_archivo',
                            'vista_previa',
                            css_class='col-sm', id='transferencia_id'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ),
            Div(
                TabHolder(
                    Tab(
                        'Actividad',
                        DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                                                 grid_opts=get_genTemaActividadDetsForm(None)),
                    ),
                ),
            )
        )

    class Meta:
        model = Gen_Tema
        fields = '__all__'
        exclude = ['tem_estado']
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data




###################################################


def get_genMultimediaFileDetsForm(cart_id):
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions(allowEdit=False)
    opts.grid_id = 'multimedia_file_grid'
    opts.grid_title = 'Respuesta'
    vista_previa = CharField(label="Vista previa", required=False)

    # DropdownList para poner en una celda de la grid
    # print('hola buenas tardes')
    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]
    opts.gridOptions['toolbar'] = ['Add', 'Edit', 'Delete', 'Update', 'Cancel']
    # opts.gridOptions['toolbarText'] = {
    #     Add: 'Añadir',
    #     edit: 'Editar',
    #     delete: 'Eliminar',
    #     update: 'Actualizar',
    #     cancel: 'Cancelar'
    # }

    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            # 'visible': True,
            # 'width': 100,
            'isPrimaryKey': True,
            'editable': False,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'muar_id',
            'visible': True,
            'width': 1,
        },
        {
            'field': 'muar_ruta',
            'isPrimaryKey': True,
            'headerText': Gen_MultimediaFile._meta.get_field('muar_ruta').verbose_name,
            'headerName': Gen_MultimediaFile._meta.get_field('muar_ruta').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': False},
            'width': 100,

            'edit': {
                'create': 'crear',
                'read': 'leer',
                'destroy': 'destruir',
                'write': 'escribir'
            },
        },
        {
            'field': 'muar_tipo',
            'headerText': Gen_MultimediaFile._meta.get_field('muar_tipo').verbose_name,
            'headerName': Gen_MultimediaFile._meta.get_field('muar_tipo').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'visible': True,
            'width': 1,

            'edit': {
                'create': 'creardos',
                'read': 'leerdos',
                'destroy': 'destruirdos',
                'write': 'escribirdos'
            },
        },
        {
            'field': 'muar_formato',
            'headerText': Gen_MultimediaFile._meta.get_field('muar_formato').verbose_name,
            'headerName': Gen_MultimediaFile._meta.get_field('muar_formato').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': True},
            'visible': True,
            'width': 1,

            'edit': {
                'create': 'creartres',
                'read': 'leertres',
                'destroy': 'destruirtres',
                'write': 'escribirtres'
            },

        },
        {
            'field': 'vista_previa',
            'headerText': 'Vista Previa',
            'headerName': 'Vista Previa',
            'width': 100,
            'visible': False,
            # 'template': '<h1>${arch}</h1>',
        },
        {
            'field': '_action',
            'visible': True,
            'width': 1,
            'edit': {'params': {'value': 'N'}},
            'defaultValue': 'N',
        }
    ]
    opts.gridOptions['toolbarClick'] = 'toolbarClick'
    opts.gridOptions['rowDataBound'] = 'rowDataBound'


    if True:
        global ContadorControl
        ContadorControl = ContadorControl + 1
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 	cart.cart_id, cart.cart_descripcion, mul_ar.muar_id, mul_ar.muar_ruta, 
	            mul_ar.muar_tipo, mul_ar.muar_formato, null vista_previa
                FROM gen.carta  AS cart
                LEFT JOIN gen.carta_mult  AS cart_mul ON cart.cart_id = cart_mul.camu_cart_id 
                LEFT join gen.multimedia_archivos AS mul_ar on cart_mul.camu_muar_id = mul_ar.muar_id 
                WHERE  cart.cart_id = %s AND cart.cart_estado = 1 
                ORDER BY cart.cart_id, mul_ar.muar_id""",
                           [cart_id])
            data = dictfetchall(cursor)

        # print('data ', jue_id, ContadorControl , data)

        data_list = []
        cont = 1

        for row in data:
            l_row_dict = row
            l_row_dict['_action'] = None
            l_row_dict['id'] = cont
            cont = cont + 1
            data_list.append(l_row_dict)
        opts.gridOptions['dataSource'] = data_list
        # opts.gridOptions['dataSource'] = data_list2

        # print('act_id tabla Respuesta : ', jue_id)
        # print(data_list)
        # print(data_list2)
    else:
        opts.gridOptions['dataSource'] = []
    return opts



####################################################
# Autor: Kevin Campoverde
# Fecha: 28/12/2023
# Descripción: Formulario para la opción 'Juego Multimedia'.
class Gen_CartaForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(Gen_CartaForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['cart_descripcion'].required = True
        self.fields['cart_descripcion'].widget.attrs['autofocus'] = True

        # Cambiar atributos especificos
        rol_usuario_actual = self.initial.get('rol_id')
        usuario_actual = self.initial.get('usuario_id')

        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label  # .lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        self.helper.label_class = 'col-sm-4 text-right form-control-sm'
        self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Div(
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('cart_descripcion',
                            css_class='col-sm'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ),
            Div(
                TabHolder(
                    Tab(
                        'Archivo de Imagen',
                        DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                                                 grid_opts=get_genMultimediaFileDetsForm(None)),
                    ),
                ),
            )
        )

    class Meta:
        model = Gen_Carta
        fields = '__all__'
        widgets = {}

    def clean(self):
        # super(Gen_AsignaturaForm, self).clean()
        form_data = self.cleaned_data
        return form_data



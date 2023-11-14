# Autor: Bryan Amaya
# Fecha: 19/12/2022 20:00
# Descripción: Aqui se almacenarán todos los elementos para hacer los CRUDs como:
#               - Formularios
#               - Grids (usando la libreria syncfunsion) para cuando se requiera cabecera-detalle
#               - Choices para generar datos estandarizados
# Form OpcionForm, InformaciondetalleForm
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django.forms import ModelForm
from django.forms import *
from apps.sis.models import Sis_Rol
from apps.sis.models import Sis_Usuario
from apps.sis.models import *
from core.crispy_layouts import DivHeaderWithButtons, DivGridHeaderWithButtons
from vars.css import Form_CSS
from vars.js import SyncFusionGridOptions
from vars.msg import CRUD_MSG
from apps.gen.models import *
from django.contrib.auth.models import User
from apps.sis.models import Sis_Informacion
import re
from django.utils.html import mark_safe
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget


# *** FORMULARIOS *** #

# Formulario para Gen_Categoria
# Autor: Bryan Amaya
def get_sisOpcionRolDetsForm(opc_id):
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions()
    opts.grid_id = 'opcionrol_grid'
    opts.grid_title = 'OpcionRol'
    # DropdownList para poner en una celda de la grid

    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]
    # DropdownList para poner en una celda de la grid
    lov_rol = list(Sis_Rol.objects.filter(rol_estado=1).values("rol_id", "rol_nombre"))
    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            'isPrimaryKey': True,
            'editable': False,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'oro_id',
            'visible': True,
            'width': 1,
        },
        {'field': 'rol_id',
         'headerText': 'rol',
         'headerName': 'rol',
         'dataSource': lov_rol,
         'foreignKeyField': 'rol_id',
         'foreignKeyValue': 'rol_nombre',  # MOSTRAR USUARIO,
         'validationRules': {'required': True}
         },
        {
            'field': 'oro_esactivo',
            'headerText': Sis_OpcionRol._meta.get_field('oro_esactivo').verbose_name,
            'headerName': Sis_OpcionRol._meta.get_field('oro_esactivo').verbose_name,
            'sortable': True,
            'filter': True,
            'textAlign': 'Center',
            'allowEditing': True,
            'editType': "booleanedit",
            'type': 'boolean',
            'dataSource': lov_yes_no,
            'foreignKeyField': 'id',
            'foreignKeyValue': 'name',
            'defaultValue': 'True',  # Establecer el valor predeterminado a True
            # 'displayAsCheckBox': False,
            'width': 100,

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
        data = Sis_OpcionRol.objects.filter(opc_id=opc_id, oro_estado=1).only("oro_id",
                                                                              "rol_id",
                                                                              "oro_esactivo")
        data_list = []
        cont = 1
        for row in data:
            l_row_dict = row.__dict__
            del l_row_dict['_state']
            l_row_dict['_action'] = None
            # print('e ', l_row_dict)
            if l_row_dict['oro_esactivo'] == 1:
                l_row_dict['oro_esactivo'] = True
            else:
                l_row_dict['oro_esactivo'] = False
            l_row_dict['id'] = cont
            cont = cont + 1
            data_list.append(l_row_dict)
        opts.gridOptions['dataSource'] = data_list
        # print('opc_id tabla Sis_Rol : ', opc_id)
        # print('dat ', data_list)
    else:
        opts.gridOptions['dataSource'] = []
    return opts


def get_SisInformacionDetsForm(inf_id):
    # Instancia de la clase en donde estan las propiedades de la grid
    opts = SyncFusionGridOptions()
    opts.grid_id = 'informaciondetalle_grid'
    opts.grid_title = 'InformacionDetalle'
    # DropdownList para poner en una celda de la grid

    # Lista para selección
    lov_yes_no = [{'id': True, 'name': 'Sí'}, {'id': False, 'name': 'No'}]
    # DropdownList para poner en una celda de la grid
    # lov_rol = list(informacionDetalle.objects.filter(ind_estado=1).values("rol_id", "rol_nombre"))
    # Aqui se puede modificar las propiedades de nuestra instancia opts
    opts.gridOptions['columns'] = [
        {
            # Este campo hace referencia al PK para la tabla
            'field': 'id',
            'visible': False,
            'isPrimaryKey': True,
            'editable': False,
        },
        {
            # Este campo hace referencia a la PK de la BD
            'field': 'ind_id',
            'visible': True,
            'width': 1,
        },
        {
            'field': 'ind_nombre',
            'headerText': Sis_Informaciondetalle._meta.get_field('ind_nombre').verbose_name,
            'headerName': Sis_Informaciondetalle._meta.get_field('ind_nombre').verbose_name,
            'sortable': True,
            'allowEditing': True,
            'validationRules': {'required': True},
            'width': 100,
        },
        {
            'field': 'ind_descripcion',
            'headerText': Sis_Informaciondetalle._meta.get_field('ind_descripcion').verbose_name,
            'headerName': Sis_Informaciondetalle._meta.get_field('ind_descripcion').verbose_name,
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
            'field': 'ind_descripcion_seguridad',
            'headerText': Sis_Informaciondetalle._meta.get_field('ind_descripcion').verbose_name,
            'headerName': Sis_Informaciondetalle._meta.get_field('ind_descripcion').verbose_name,
            'allowEditing': True,
            'validationRules': {'required': False},
            'width': 1,
            'visible': True,
            'edit': {
                # 'create': 'creardos',
                'read': 'leerdos',
                # 'destroy': 'destruirdos',
                # 'write': 'escribirdos'
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
    if True:
        # data = Sis_Rol.objects.filter(rol_id=rol_id, rol_estado=1).only("rol_nombre")
        data = Sis_Informaciondetalle.objects.filter(inf_id=inf_id, ind_estado=1).only("ind_id",
                                                                                       "ind_nombre",
                                                                                       "ind_descripcion",
                                                                                       "ind_estado"
                                                                                       )

        data_list = []
        cont = 1
        for row in data:
            l_row_dict = row.__dict__
            del l_row_dict['_state']
            l_row_dict['_action'] = None
            l_row_dict['id'] = cont
            l_row_dict['ind_descripcion_seguridad'] = l_row_dict['ind_descripcion']
            cont = cont + 1
            data_list.append(l_row_dict)
        print('aaaa ', data_list)
        opts.gridOptions['dataSource'] = data_list
        # print('opc_id tabla Gen_Act : ', tem_id)
        # print(data_list)
    else:
        opts.gridOptions['dataSource'] = []
    return opts


# Autor: Bryan Amaya
class Sis_OpcionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Sis_OpcionForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['opc_idpadre'].required = False
        self.fields['opc_codigov'].required = True
        self.fields['opc_descripcion'].required = False
        self.fields['opc_url'].required = True
        self.fields['opc_icono'].required = False
        self.fields['opc_tipo'].required = True
        self.fields['opc_orden'].required = True
        self.fields['opc_idpadre'].widget.attrs['autofocus'] = True
        # Cambiar atributos genericos
        for form in self.visible_fields():
            form.field.widget.attrs['placeholder'] = Form_CSS.fields_placeholder + form.field.label.lower()
            form.field.widget.attrs['autocomplete'] = Form_CSS.fields_autocomplete
            form.field.widget.attrs['class'] = Form_CSS.fields_attr_class
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = Form_CSS.getFormID(self)
        # self.helper.attrs = Form_CSS.form_attrs
        self.helper.form_tag = True
        self.helper.form_error_title = Form_CSS.form_err_title
        self.helper.form_class = Form_CSS.form_class
        # self.helper.label_class = Form_CSS.fields_label_class
        # self.helper.field_class = Form_CSS.fields_field_class
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
                        Div('opc_codigov',
                            'opc_nombre',
                            'opc_descripcion',
                            'opc_url',
                            css_class='col-sm'
                            ),
                        Div('opc_idpadre',
                            'opc_orden',
                            'opc_tipo',
                            'opc_icono',
                            css_class='col-sm', id='transferencia_id'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ), Div(
                TabHolder(
                    Tab(
                        'OpcionRol',
                        DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                                                 grid_opts=get_sisOpcionRolDetsForm(None)),
                    ),

                ),
            )
        )

    class Meta:
        model = Sis_Opcion
        fields = '__all__'
        exclude = ['opc_estado']
        widgets = {}

    def clean(self):
        # super(Gen_CategoriaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Bryan Amaya
class Sis_InformaciondetalleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Sis_InformaciondetalleForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['inf'].required = True
        self.fields['ind_nombre'].required = True
        self.fields['ind_descripcion'].required = False
        self.fields['inf'].widget.attrs['autofocus'] = True
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
                Div('inf',
                    'ind_nombre',
                    'ind_descripcion',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    class Meta:
        model = Sis_Informaciondetalle
        fields = '__all__'
        exclude = ['ind_estado']
        widgets = {}

    def clean(self):
        # super(Gen_CategoriaForm, self).clean()
        form_data = self.cleaned_data
        return form_data


# Autor: Dre
# Fecha: 18/12/2022 13:00
# Descripción: Aqui se almacenarán todos los elementos para hacer los CRUDs como:
#               - Formularios
#               - Grids (usando la libreria syncfunsion) para cuando se requiera cabecera-detalle
#               - Choices para generar datos estandarizados

# *** FORMULARIOS *** #

# Formulario para Sis Información
class Sis_InformacionForm(ModelForm):
    # inf_descripcion = CharField(widget=CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super(Sis_InformacionForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['inf_nombre'].required = True
        self.fields['inf_descripcion'].required = False
        self.fields['inf_tipo'].required = True
        self.fields['inf_nombre'].widget.attrs['autofocus'] = True
        self.fields['inf_tipo'].choices = self.available_tipo_choices()
        # Cambiar atributos genericos
        for form in self.visible_fields():
            if form.field.label:
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
                Div('inf_nombre',
                    'inf_descripcion',
                    'inf_tipo',
                    css_class='card-body'
                    ),
                css_class='card'
            ), Div(
                TabHolder(
                    Tab(
                        'Detalle',
                        DivGridHeaderWithButtons(instance_pk=self.instance.pk,
                                                 grid_opts=get_SisInformacionDetsForm(None)),
                    ),
                ),
            )
        )

    def available_tipo_choices(self):
        used_tipos = Sis_Informacion.objects.exclude(pk=self.instance.pk if self.instance else None).values_list(
            'inf_tipo', flat=True)
        return [(value, label) for value, label in CHOICES_TIPO_INF if value not in used_tipos]

    class Meta:
        model = Sis_Informacion
        fields = '__all__'
        exclude = ['inf_estado']
        widgets = {}

    def clean(self):
        # super(Sis_InformacionForm, self).clean()
        form_data = self.cleaned_data
        return form_data


class Sis_RolForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sis_RolForm, self).__init__(*args, **kwargs)
        # Cambiar atributos especificos
        self.fields['rol_nombre'].required = True
        self.fields['rol_tipo'].required = True
        self.fields['rol_nombre'].widget.attrs['autofocus'] = True
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
                Div('rol_nombre',
                    'rol_tipo',
                    css_class='card-body'
                    ),
                css_class='card'
            ),
        )

    def clean_rol_tipo(self):
        rol_tipo = self.cleaned_data['rol_tipo']

        try:
            rol_tipo_int = int(rol_tipo)
            if rol_tipo_int <= 0:
                raise forms.ValidationError("Ingrese un número positivo válido.")
        except ValueError:
            raise forms.ValidationError("Ingrese un número válido.")

        return rol_tipo_int

    class Meta:
        model = Sis_Rol
        fields = '__all__'
        exclude = ['rol_estado']
        widgets = {}

    def clean(self):
        # super(Sis_RolForm, self).clean()
        form_data = self.cleaned_data
        return form_data


class Sis_UsuarioForm(ModelForm):
    antigua_password = CharField(label="Ultima Contraseña", required=True)
    nueva_password = CharField(label="Nueva Contraseña", required=True)
    password2 = CharField(label="Repita la Contraseña", required=True)

    # vista_rol = CharField(label="Nueva Contraseña", required=True)
    def __init__(self, *args, **kwargs):
        super(Sis_UsuarioForm, self).__init__(*args, **kwargs)
        contra = self.initial.get('password')
        rol_usuario_actual = self.initial.get('rol_id')
        # print(rol_usuario_actual)
        if contra:

            self.fields['nueva_password'].required = False
            self.fields['antigua_password'].required = False
            self.fields['nueva_password'].widget = PasswordInput()
            self.fields['password2'].widget = PasswordInput()
            self.fields['password'].widget = HiddenInput()
            self.fields['antigua_password'].widget = HiddenInput()
            self.fields['rol'].required = False
            # self.fields['rol'].widget = HiddenInput()
            # print('avanzas', contra)
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            # vista_previa_html = f'<img src="{mul_archivo.url}" alt="Vista previa de la imagen">'
            # self.fields['vista_previa'].initial = mark_safe(f'{mul_archivo}')

            if rol_usuario_actual == 2:
                self.fields['antigua_password'].required = False
                self.fields['nueva_password'].required = False
                self.fields['antigua_password'].widget = PasswordInput()
                self.fields['password2'].widget = HiddenInput()
        else:
            self.fields['nueva_password'].widget = HiddenInput()
            self.fields['antigua_password'].widget = HiddenInput()
            self.fields['nueva_password'].required = False
            self.fields['antigua_password'].required = False
            self.fields['password2'].widget = PasswordInput()
            self.fields['rol'].required = True
            # print('no avanzas')
            # self.fields['vista_previa'].initial = ''
        # Cambiar atributos especificos
        # self.fields['rol'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['institucion'].required = False
        self.fields['curso'].required = False
        self.fields['password'].required = False
        self.fields['password2'].required = False
        self.fields['is_staff'].required = False
        self.fields['is_superuser'].required = False
        self.fields['is_active'].required = False
        # self.fields['groups'].required = False
        # self.fields['user_permissions'].required = False
        self.fields['date_joined'].required = False
        self.fields['first_name'].widget.attrs['autofocus'] = True
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
                # DivHeaderWithButtons(instance_pk=self.instance.pk, permisos=self.PERMISOS),
                DivHeaderWithButtons(instance_pk=self.instance.pk,
                                     permisos={'oro_agregar': 1, 'oro_modificar': 1, 'oro_eliminar': 1,
                                               'oro_imprimir': 0}),
                Div(
                    Div(
                        Div('username',
                            'first_name',
                            'last_name',
                            'institucion',
                            'curso',
                            'rol',
                            css_class='col-sm'
                            ),
                        Div('email',
                            'antigua_password',
                            'password',
                            'nueva_password',
                            'password2',
                            'is_active',
                            'is_staff',
                            'is_superuser',
                            # 'groups',
                            # 'user_permissions',
                            'date_joined',
                            css_class='col-sm', id='transferencia_id'
                            ),
                        css_class='row'
                    ),
                    css_class='card-body', id='body_id'
                ),
                css_class='card'
            ))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[A-Za-zñÑáéíóúÁÉÍÓÚ ]+$', first_name):
            raise forms.ValidationError(
                "El nombre solo debe contener letras A-Z, a-z, ñ, tildes en vocales y máximo un espacio.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[A-Za-zñÑáéíóúÁÉÍÓÚ ]+$', last_name):
            raise forms.ValidationError(
                "El apellido solo debe contener letras A-Z, a-z, ñ, tildes en vocales y máximo un espacio.")
        return last_name

    class Meta:
        model = User
        fields = '__all__'
        # exclude = []
        widgets = {
            'date_joined': HiddenInput(),
            'is_staff': HiddenInput(),
            # 'groups' : HiddenInput(),
            'is_superuser': HiddenInput(),
            'password': PasswordInput(),
            'password2': PasswordInput(),
            # 'user_permissions' : HiddenInput(),

        }

    def clean(self):
        # super(Sis_UsuarioForm, self).clean()
        form_data = self.cleaned_data
        return form_data


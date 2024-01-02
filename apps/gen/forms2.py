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
            'field': 'muar_id',
            'visible': True,
            'width': 1,
        },
        {
            'field': 'muar_ruta',
            'isPrimaryKey': True,
            'headerText': Gen_Multimedia._meta.get_field('muar_ruta').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('muar_ruta').verbose_name,
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
            'headerText': Gen_Multimedia._meta.get_field('muar_tipo').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('muar_tipo').verbose_name,
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
            'field': 'muar_formato',
            'headerText': Gen_Multimedia._meta.get_field('muar_formato').verbose_name,
            'headerName': Gen_Multimedia._meta.get_field('muar_formato').verbose_name,
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
    return opts

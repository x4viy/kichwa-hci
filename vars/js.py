import json

datatable_opts = {
    'responsive': True,
    'lengthChange': True,
    'autoWidth': False,
    'paging': True,
    'searching': True,
    'ordering': True,
    'info': True,
    'order': [[1, "asc"]],
    'columnDefs': [
        {
            'targets': [0],
            'visible': True,
            'orderable': False,
            'searchable': False,
            'width': '4%',
        }
    ],
    'drawCallback': None,
    'pageLength': 25,
    'pagingType': 'full_numbers',
    'buttons': ["colvis", "copy", "excel", "pdf", "print"],
    'dom':
        "<'row'<'col-sm-3'l><'col-sm-5 text-center'B><'col-sm-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'i><'col-sm-7'p>>",
}
datatable_opts = {
    'responsive': True,
    'lengthChange': True,
    'autoWidth': False,
    'paging': True,
    'searching': True,
    'ordering': True,
    'info': True,
    'order': [[1, "asc"]],
    'columnDefs': [
        {
            'targets': [0],
            'visible': True,
            'orderable': False,
            'searchable': False,
            'width': '4%',
        }
    ],
    'drawCallback': None,
    'pageLength': 25,
    'pagingType': 'full_numbers',
    'buttons': ["colvis", "copy", "excel", "pdf", "print"],
    'dom':
        "<'row'<'col-sm-3'l><'col-sm-5 text-center'B><'col-sm-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'i><'col-sm-7'p>>",
}
datatableGroup_opts = {
    'responsive': True,
    'lengthChange': True,
    'autoWidth': False,
    'paging': True,
    'searching': True,
    'ordering': True,
    'info': True,
    'order': [[1, "asc"]],
    'columnDefs': [
        {
            'targets': [0],
            'visible': True,
            'orderable': False,
            'searchable': False
        }
    ],
    'drawCallback': 'fn_drawCallback',
    'pageLength': 25,
    'pagingType': 'full_numbers',
    'buttons': ["colvis", "copy", "excel", "pdf", "print"],
    'dom':
        "<'row'<'col-sm-3'l><'col-sm-5 text-center'B><'col-sm-4'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-5'i><'col-sm-7'p>>",
}

# funciones edit options
crearFn = 'crearFn'
leerFn = 'leerFn'
destruirFn = 'destruirFn'
fechaFn = 'fechaFn'


# Propiedades de la grid
class SyncFusionGridOptions(object):
    def __init__(self, model_id="grid", allowEdit=True, allowAdd=True, allowDelete=True):
        self.allowEdit = allowEdit
        self.allowAdd = allowAdd
        self.allowDelete = allowDelete
        self.allowPaging: True
        self.grid_id = "id_grid_" + str(model_id)
        self.grid_title = ""
        self.gridOptions = {
            'commandClick': 'commandClick',
            'columns': {},
            'aggregates': {},
            'dataSource': [],
            'locale' : 'es-EC',
            'groupSettings': None,
            'allowGrouping': False,
            'sortSettings': None,
            'allowSorting': False,
            'editSettings': {'allowEditing': allowEdit, 'allowAdding': allowAdd, 'allowDeleting': allowDelete,
                             'newRowPosition': 'Bottom'},
            'allowExcelExport': False,
            'toolbar': ['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'Search'],
            'actionBegin': None,
            'actionComplete': None,
            'toolbarClick': None,
            'rowDataBound': None,
            'formatSettings': None,
            # 'width': '100%',
            # 'height': 315
        }
        self.div_style = ""

    def __set_addNewRowFnData(self):
        pass

    def to_JSON(self):
        self.__set_addNewRowFnData()
        return self.__dict__


# Propiedades de la grid
class SyncFusionGridOptions_NotSearch(object):
    def __init__(self, model_id="grid", allowEdit=True, allowAdd=True, allowDelete=True):
        self.allowEdit = allowEdit
        self.allowAdd = allowAdd
        self.allowDelete = allowDelete
        self.allowPaging: True
        self.grid_id = "id_grid_" + str(model_id)
        self.grid_title = ""
        self.gridOptions = {
            'commandClick': 'commandClick',
            'columns': {},
            'aggregates': {},
            'dataSource': [],
            'locale': 'es',
            'groupSettings': None,
            'allowGrouping': False,
            'editSettings': {'allowEditing': allowEdit, 'allowAdding': allowAdd, 'allowDeleting': allowDelete,
                             'newRowPosition': 'Bottom'},
            'allowExcelExport': False,
            'toolbar': ['Add', 'Edit', 'Delete', 'Update', 'Cancel'],
            'actionBegin': None,
            'actionComplete': None,
            'toolbarClick': None,
            'rowDataBound': None,
            # 'height': 315
        }
        self.div_style = ""

    def __set_addNewRowFnData(self):
        pass

    def to_JSON(self):
        self.__set_addNewRowFnData()
        return self.__dict__


class GridOptions(object):
    def __init__(self, model_id="grid"):
        self.grid_id = "id_grid_" + str(model_id)
        self.grid_title = ""
        self.gridOptions = {
            'columnDefs': None,
            'rowData': None,
            'defaultColDef': {
                'flex': 1,
                'minWidth': 110,
                'resizable': True},
            'enterMovesDown': True,
            'enterMovesDownAfterEdit': True,
            'undoRedoCellEditing': True,
            'undoRedoCellEditingLimit': 10,
            'rowSelection': 'multiple',
            'animateRows': True,
            'locale': 'es',
            'onCellEditingStarted': "function(event) {}",
            'components': ''
        }
        self.cols_data_fns = None
        self.addNewRow = {
            'allowAddNewRow': False,
            'addNewRowOnLoad': False,
            'newRowData': None,
            'grid_btn_add': "id_btn_addrow_" + str(model_id),
            'addNewRowFnDataJS': None
        }
        self.removeSelectedRows = {
            'alloRemoveSelectedRows': False,
            'grid_btn_rem': "id_btn_remrow_" + str(model_id)
        }
        self.div_style = "height: 200px; width:auto;"

    def __set_addNewRowFnData(self):
        if self.addNewRow['newRowData'] is not None:
            self.addNewRow['addNewRowFnDataJS'] = "function createNewRowData() { return " + str(
                json.dumps(self.addNewRow['newRowData'])) + "}"
        else:
            self.addNewRow['addNewRowFnDataJS'] = "function createNewRowData() {}"

    def to_JSON(self):
        self.__set_addNewRowFnData()
        return self.__dict__


class SyncFusionPivotGridOptions(object):
    def __init__(self, model_id="PivotTable"):
        self.grid_id = model_id
        self.grid_title = ""
        self.gridOptions = {
            'dataSourceSettings': {
                'expandAll': False,
                'locale': 'es',
                'dataSource': [],
                'columns': {},
                'values': {},
                'rows': [],
                'filters': [],
                'formatSettings': {},
                'enableSorting': True,
                'allowLabelFilter': True,
                'allowValueFilter': True,
                'drilledMembers': {},
                'selectionSettings': {'persistSelection': True},
                'showFieldList': True,
            },
            'locale': 'es',
            'enginePopulated': None
            # 'height' : 350,
            # 'div_style' : "",
        }
        self.div_style = ""

    def __set_addNewRowFnData(self):
        pass

    def to_JSON(self):
        self.__set_addNewRowFnData()
        return self.__dict__

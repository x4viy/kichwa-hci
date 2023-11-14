from datetime import datetime


class Form_CSS:
    form_attrs = {'action': '.', 'onkeydown': "return event.key != 'Enter';"}
    form_err_title = 'Errores'
    form_class = 'form-horizontal'
    fields_autocomplete = 'off'
    fields_placeholder = ''
    fields_attr_class = 'form-control-border form-control-sm'  # afecta a la clase del input
    fields_label_class = 'col-sm-2 text-right form-control-sm'
    fields_field_class = 'col-sm-3 row'  # afecta al div contenedor del input
    fields_field_class_5 = 'col-sm-5 row'  # afecta al div contenedor del input
    fields_field_class_6 = 'col-sm-6 row'  # afecta al div contenedor del input
    fields_date_format = '%d/%m/%Y'
    fields_date_opts = {'locale': 'es-us', }
    fields_current_date = datetime.now().strftime(fields_date_format)

    def getFormID(obj):
        return 'form_' + obj.__class__.__name__ + '_id'

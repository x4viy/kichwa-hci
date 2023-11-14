class CRUD_MSG:
    CREATE = 'Registro creado'
    SAVE = 'Registro actualizado'
    DELETE = 'Registro eliminado'
    FIELD_EMPTY = 'Complete este campo'
    CODIGOV_DUPLICADO = 'El código ya está registrado'
    CODIGOV_DUPLICADO_DET = 'El código del detalle está repetido'
    UNIMEDIDA_DUPLICADO_DET = 'La unidad de medida del detalle está repetido'
    CODIGOV_REGISTRADO_DET = 'El código del detalle ya está registrado'
    NOMBRE_DUPLICADO = 'El nombre ya está registrado'
    FECHAFIN_ERROR_MENOR = 'La fecha de fin no puede ser menor que la fecha de inicio'
    SIN_REGISTROS = 'No se encontraron registros de acuerdo a las condiciones indicadas'
    ERROR_SERVER = 'Internal Server Error: '
    REQUIRED = 'Este campo es obligatorio.'
    OUTOFSTOCK = 'Cantidad no disponible.'
    DETAILNOTEMPTY = 'El detalle no puede estar vacio.'
    DETAILCERO = 'El detalle tiene valores en cero o vacios.'

class global_formats:
    format_coin = '#,###.#0'
    decimals_max = 2

class FORMS_TEXT:
    FEC_DESDE = 'Fecha desde: '
    FEC_HASTA = 'Fecha hasta: '

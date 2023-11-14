# Fecha: 03/05/2022
# Objetivo: Codigos de los menus para imprimir y ver permisos
# Autor: LG

class con_man:
    # Mantenimientos
    Cambio_patrimonio = 'CON_MAN02'
    Cuentas = 'CON_MAN03'
    Pl_fl_efectivo = 'CON_MAN04'

class con_pro:
    # Procesos
    Act_des_comp = 'CON_PRO01'
    Apert_cierre_mes = 'CON_PRO02'
    Movimientos = 'CON_PRO03'
    Asiento_inicial = 'CON_PRO04'
    Asiento_cierre_anual = 'CON_PRO05'

class con_rep:
    # Reportes
    print_comprobantes = 'CON_REP01'
    Diario = 'CON_REP02'
    Cambio_Patrimonio = 'CON_REP03'
    Est_Sit_Financiera = 'CON_REP04'
    Mayores = 'CON_REP05'
    Saldo_Mayores = 'CON_REP06'
    Balance_Comprobacion = 'CON_REP07'
    Estado_Resultados = 'CON_REP08'
    Fl_Efectivo = 'CON_MAN01'

class adm_man:
    periodo = 'ADM_PRO01'
    sucursal = 'ADM_GEN02'
    empresa = 'ADM_GEN03'
    documento = 'ADM_GEN04'
    motivo_not_deb = 'ADM_GEN01'
    parametros = 'ADM_MAN01'
    formapago = 'ADM_MAN02'
    puntoemision = 'ADM_MAN03'
    # Autor: dre
    # Fecha: 21/11/2022 8:20
    # Descripción: Códigos de los menus para otorgar permisos - Proceso Administración
    aperturaCierrePeriodo = 'ADM_PRO02'

class ven_man:
    actividad_cliente = 'VEN_MAN03'
    estado_cliente = 'VEN_MAN02'
    tipo_cliente = 'VEN_MAN04'
    zona = 'VEN_MAN05'
    vendedor = 'VEN_MAN01'
    grupo_precio = 'VEN_MAN06'
    cliente = 'VEN_MAN07'

class ven_pro:
    anticipo = 'VEN_PRO01'
    cotizacion = 'VEN_PRO02'


# Autor: dre
# Fecha: 18/05/2022 9:55
# Descripción: Códigos de los menus para otorgar permisos - Inventarios
class inv_man:
    # Mantenimientos
    Modelo = "INV_MAN01"
    Marca = "INV_MAN02"
    Bodega ="INV_MAN03"
    UnidadMedida = "INV_MAN04"
    TipoItem = "INV_MAN05"
    CampoItem = "INV_MAN06"
    Linea ="INV_MAN07"
    Item = "INV_MAN08"
    ActivarDesactivar_Item = "INV_MAN09"
    # Procesos
    transaccion = "INV_PRO01"
    AperturaCierreMes = "INV_PRO02"
    AperturaPeriodo = "INV_PRO03"
    ActualizarCosto = "INV_PRO04"
    # Reportes
    kardexEmpresa = "INV_REP01"
    kardexBodega = "INV_REP02"
    ExistenciasCostos = "INV_REP03"




# Autor: dre
# Fecha: 08/07/2022 10:00
# Descripción: Códigos de los menus para otorgar permisos - Impuestos

class imp_man:
    # Mantenimientos
    tipoTransaccion = "IMP_MAN12"
    tipoIdentificacion = "IMP_MAN07"
    secuencialTransaccion = "IMP_MAN03"
    tipoPago = "IMP_MAN01"
    retencionFuente = "IMP_MAN02"
    tipoSustento = "IMP_MAN04"
    tipoComprobante = "IMP_MAN05"
    pctRetencionIva = "IMP_MAN16"
    tipoImpuesto = "IMP_MAN20"
    pctIva = "IMP_MAN17"
    formaPago = "IMP_MAN18"
    tipoIdProveedor = "IMP_MAN19"
    tipoUbicacion = "IMP_MAN08"
    ubicacion = "IMP_MAN09"
    paraisoFiscal = "IMP_MAN13"
    tipoRegimenFiscal = "IMP_MAN14"
    tipoEmisionFactura = "IMP_MAN10"
    tipoCompensacion = "IMP_MAN11"
    fe_tipoEmision = "IMP_MAN06"
    fe_tipoAmbiente = "IMP_MAN15"

    # Procesos

    # Reportes

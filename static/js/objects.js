// Clase base que representa un item del detalle
class ItemDetalle {
    constructor(ite_id, ite_codigov, cantidad, precio, tig, dsctopct = 0.0,
                iceval = 0.0, escala = {'moneda': 2, 'costo': 6},
                action = 'N', det_id = null) {
        // Parametros de control
        this.id = 0;
        this.escala = escala;
        this._action = action;
        // Atributos del item
        this.ite_id = ite_id;
        this.ite_codigov = ite_codigov;
        this.det_cantidad = this.redondear(parseFloat(cantidad), escala.costo);
        this.det_dsctopct = this.redondear(parseFloat(dsctopct), escala.moneda);
        this.det_iceval = this.redondear(parseFloat(iceval), escala.moneda);
        this.det_precio = this.redondear(parseFloat(precio), escala.costo);
        this.tig_id = tig;
        this.det_id = det_id;
        // Atributos del item (calculados)
        this.det_dsctoval = this.calcDsctoVal();
        this.det_precio_dscto = this.calcPrecUnitDscto();
        this.det_dsctotot = this.calcDsctoTot();
        this.det_total = this.calcTotal();

    }

    setCantidad(cantidad) {
        this.det_cantidad = this.redondear(parseFloat(cantidad), this.escala.costo);
        this.det_dsctotot = this.calcDsctoTot();
        this.det_total = this.calcTotal();
    }

    setDsctoPct(dsctopct) {
        this.det_dsctopct = this.redondear(parseFloat(dsctopct), this.escala.moneda);
        this.det_dsctoval = this.calcDsctoVal();
        this.det_precio_dscto = this.calcPrecUnitDscto();
        this.det_dsctotot = this.calcDsctoTot();
        this.det_total = this.calcTotal();
    }

    calcDsctoVal() {
        return this.redondear((this.det_dsctopct === 0) ? 0 : this.det_precio * this.det_dsctopct / 100, this.escala.costo);
    }

    setPrecio(precio) {
        this.det_precio = precio;
        this.det_dsctoval = this.calcDsctoVal();
        this.det_precio_dscto = this.calcPrecUnitDscto();
        this.det_dsctotot = this.calcDsctoTot();
        this.det_total = this.calcTotal();
    }

    calcPrecUnitDscto() {
        return this.redondear(this.det_precio - this.det_dsctoval, this.escala.costo);
    }

    calcPrecSd() {
        return this.det_cantidad * this.det_precio;
    }

    calcDsctoTot() {
        if (this.det_dsctoval > 0) {
            return this.redondear(this.det_cantidad * this.det_dsctoval, this.escala.costo);
        } else {
            return 0;
        }

    }

    calcTotal() {
        return this.redondear(this.calcPrecSd() - this.calcDsctoTot(), this.escala.costo);
    }

    redondear(num, scale) {
        if (!("" + num).includes("e")) {
            return +(Math.round(num + "e+" + scale) + "e-" + scale);
        } else {
            var arr = ("" + num).split("e");
            var sig = ""
            if (+arr[1] + scale > 0) {
                sig = "+";
            }
            return +(Math.round(+arr[0] + "e" + sig + (+arr[1] + scale)) + "e-" + scale);
        }
    }

}

class ItemDetallePedido extends ItemDetalle {
    constructor(ite_id, ite_codigov, cantidad, precio, tig, dsctopct = 0.0,
                iceval = 0.0, escala, observacion = '', fecha_entrega = null, action = 'N', det_id = null) {
        super(ite_id, ite_codigov, cantidad, precio, tig, dsctopct, iceval, escala, action, det_id);

        this.det_observacion = observacion;
        this.det_fecha_entrega = fecha_entrega;
    }

    setFechaEntrega(fecha_entrega) {
        this.det_fecha_entrega = fecha_entrega;
    }

    setObservacion(observacion) {
        this.det_observacion = observacion;
    }

}

class ItemDetalleFacturacion extends ItemDetalle {
    constructor(ite_id, ite_codigov, cantidad, precio, tig, dsctopct = 0.0,
                iceval = 0.0, escala, bodega, observacion = '', action = 'N', det_id = null) {

        super(ite_id, ite_codigov, cantidad, precio, tig, dsctopct, iceval, escala, action, det_id);


        this.det_bodega = bodega;
        this.det_observacion = observacion;

    }

    setBodega(bodega) {
        this.det_bodega = bodega;
    }

    setObservacion(observacion) {
        this.det_observacion = observacion;
    }

}

class Documento {
    constructor(items, prefijo_tabla, escala = 2) {
        // Detalle
        this.items = items; // Array de items
        // Cabecera
        this.subtot_coniva = 0;
        this.subtot_siniva = 0;
        this.subtot_exeiva = 0;
        this.subtot_noobjiva = 0;
        this.subtotsd_coniva = 0;
        this.subtotsd_siniva = 0;
        this.subtotsd_exeiva = 0;
        this.subtotsd_noobjiva = 0;
        this.subtotalsd = 0;
        this.dsctodet = 0;
        this.dsctopct = 0;
        this.dsctoval = 0;
        this.subtotal = 0;
        this.dsctotot = 0;
        this.iceval = 0;
        this.ivaval = 0;
        this.total = 0;
        // Prefijo de la tabla cabecera
        this.prefijo_tabla = prefijo_tabla;
        // Escala de los subtotales
        this.escala = escala;

    }

    // Add secuencial index to items
    addIndexToItems() {
        let i = 1;
        this.items.forEach(item => {
            item.id = i;
            i++;
        });
    }

    // Append arrays
    appendItems(items) {
        this.items = this.items.concat(items);
    }

    getDsctoPct() {
        var dsctoPctInput = document.querySelector('#id_' + this.prefijo_tabla + '_dsctopct');
        return parseFloat(dsctoPctInput.value);
        //return this.dsctopct;
    }

    calcDsctoVal() {
        return this.subtotalsd * this.dsctopct / 100;
    }

    setDsctoPct(valor) {
        this.dsctopct = valor;
    }

    // Métodos para calcular los valores de los atributos
    calcSubtotales() {
        // Cálculo de valores por subsección
        this.calcSubtotaleSd();
        this.calcSubtotalesCd();
        this.calcTotales();
        // Carga valores en los campos
        this.updateSubtotales();
    }

    // Calcula subtotales sin descuento
    calcSubtotaleSd() {

        for (let item of this.items) {
            if (item.tig_id === 1) {
                this.subtotsd_coniva += item.det_total;
            } else if (item.tig_id === 2) {
                this.subtotsd_siniva += item.det_total;
            } else if (item.tig_id === 3) {
                this.subtotsd_exeiva += item.det_total;
            } else {
                this.subtotsd_noobjiva += item.det_total;
            }
            // Descuento por linea
            this.dsctodet += item.det_dsctotot;
            // ICE
            this.iceval += item.det_iceval;
        }

        this.subtotalsd = this.subtotsd_coniva + this.subtotsd_siniva + this.subtotsd_exeiva + this.subtotsd_noobjiva;
    }

    calDesctSubtotales(subtotal) {
        return (subtotal - (subtotal * this.dsctopct / 100));
    }

    calcSubtotalesCd() {
        // Subtotales con descuento
        this.dsctopct = this.getDsctoPct();
        if (this.dsctopct > 0) {
            this.dsctoval = this.calcDsctoVal();
            if (this.subtotsd_coniva > 0) {
                this.subtot_coniva = this.calDesctSubtotales(this.subtotsd_coniva);
            }
            if (this.subtotsd_siniva > 0) {
                this.subtot_siniva = this.calDesctSubtotales(this.subtotsd_siniva);
            }
            if (this.subtotsd_exeiva > 0) {
                this.subtot_exeiva = this.calDesctSubtotales(this.subtotsd_exeiva);
            }
            if (this.subtotsd_noobjiva > 0) {
                this.subtot_noobjiva = this.calDesctSubtotales(this.subtotsd_noobjiva);
            }

        } else {
            this.dsctoval = 0;
            this.subtot_coniva = this.subtotsd_coniva;
            this.subtot_siniva = this.subtotsd_siniva;
            this.subtot_exeiva = this.subtotsd_exeiva;
            this.subtot_noobjiva = this.subtotsd_noobjiva;
        }

        this.subtotal = this.subtot_coniva + this.subtot_siniva + this.subtot_exeiva + this.subtot_noobjiva;
    }

    // Calcula totales
    calcTotales() {
        // Descuento total
        this.dsctotot = this.dsctodet + this.dsctoval;
        // IVA
        this.ivaval = (this.subtot_coniva + this.iceval) * 0.12;
        // Valor total
        this.total = this.subtotal + this.ivaval + this.iceval;
    }

    // Métodos para actualizar los valores de los campos del formulario
    updateSubtotales() {
        // console.log('updateSubtotales', this.items);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtot_coniva').value = this.subtot_coniva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtot_siniva').value = this.subtot_siniva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtot_exeiva').value = this.subtot_exeiva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtot_noobjiva').value = this.subtot_noobjiva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotsd_coniva').value = this.subtotsd_coniva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotsd_siniva').value = this.subtotsd_siniva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotsd_exeiva').value = this.subtotsd_exeiva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotsd_noobjiva').value = this.subtotsd_noobjiva.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotalsd').value = this.subtotalsd.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_dsctodet').value = this.dsctodet.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_dsctopct').value = this.dsctopct.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_dsctoval').value = this.dsctoval.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_subtotal').value = this.subtotal.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_dsctotot').value = this.dsctotot.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_iceval').value = this.iceval.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_ivaval').value = this.ivaval.toFixed(this.escala);
        document.querySelector('#id_' + this.prefijo_tabla + '_total').value = this.total.toFixed(this.escala);


    }

}
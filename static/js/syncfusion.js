// Autor: dre
// Fecha: 13/11/2021 02:45
// Descripción: Función para subrayar un registro cuando el estado del registro sea E
function rowDataBound(args) {
    var gridId = Object.getOwnPropertyNames(args.data)[0];
    if (args.data['_action'] === 'E' && args.data[gridId] != null) {
        args.row.classList.add('below-30');
    } else {
        args.row.style.background = '#eee';
    }
}

// Autor: dre
// Fecha: 16/12/2021 12:45
// Descripción:evento click de los botones crud
function toolbarClick(args) {
    for (var i = 0; i < grid.length; i++) {
        if (grid[i].getSelectedRecords().length > 0){
            var selectedrecords = grid[i].getSelectedRecords();
            var gridId = Object.getOwnPropertyNames(selectedrecords[0])[0];
            //Eliminar registro grid_tsust
            if (args.item.text == 'Delete') {
                args.cancel = true;
                // get the selected records.
                if (grid[i].getSelectedRowIndexes().length) {
                    if (selectedrecords[0][gridId] != null && selectedrecords[0]._action != 'E') { //si el Id es nulo y no esta en estado eliminado, lo cambia de estado a eliminado
                        grid[i].setCellValue(selectedrecords[0].id, '_action', 'E');
                    } else if (selectedrecords[0][gridId] != null && selectedrecords[0]._action === 'E') { // si el id es nulo pero si esta eliminado, lo regresa a estado normal
                        grid[i].setCellValue(selectedrecords[0].id, '_action', '');
                    } else { // si el id es nulo, elimina el registro de la grid_tsust
                        grid[i].deleteRecord();
                    }
                } else {
                    alert("No hay filas seleccionadas");
                }
                grid[i].refresh(); // refresh the grid_tsust.
                delete grid[i][0];
                break;
            }
        }
    }
}
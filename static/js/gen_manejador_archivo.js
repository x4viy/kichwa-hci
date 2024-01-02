var elem
var strm
var ruta_archivo
var extension
var fileName
var tipo_arch
var formato_arch
var contador = 0
var arreglo = []

// Cantidad
function crear() {
    console.log('CREAR');
    elem = document.createElement('input');
    elem.setAttribute('name', 'myfile');

    return elem;
}

function creardos() {
    console.log('CREARdos');
    elem2 = document.createElement('input');
    elem2.setAttribute('name', 'mytipo');
    elem2.setAttribute('value', 'Suba el archivo para determinar la extension!'); // Configura el atributo de valor (value) del elemento con el valor "ejemplo"
    elem2.setAttribute('readonly', true);
    console.log('Nombre del elemento:', elem2.getAttribute('name')); // Agregar esta línea para imprimir el nombre del elemento
    return elem2;
}

function creartres() {
    console.log('CREARtres');
    elem3 = document.createElement('input');
    elem3.setAttribute('name', 'myformato');
    elem3.setAttribute('value', 'Suba el archivo para determinar el formato!'); // Configura el atributo de valor (value) del elemento con el valor "ejemplo"
    elem3.setAttribute('readonly', true);
    console.log('Nombre del elemento:', elem3.getAttribute('name')); // Agregar esta línea para imprimir el nombre del elemento
    return elem3;
}

function leer() {
    console.log('LEER');
    console.log(fileName);
    strm = fileName;

    return strm;
}

function leerdos() {
    console.log('LEERdos');
    strm = tipo_arch;
    return strm;
}

function leertres() {
    console.log('LEERtres');
    strm = formato_arch;
    return strm;
}


function destruir() {
    console.log('DESTRUIR');
    // onFileRemove();
    extension = undefined;

}

function destruirdos() {
    console.log('DESTRUIRdos');

}

function destruirtres() {
    console.log('DESTRUIRtres');

}


function escribirtres() {
    console.log('escribirtres');
    console.log('extfinal:', extension);
    console.log('nombre:', fileName);
    var elem3 = document.querySelector('input[name="muar_formato"]'); // buscar el elemento por su atributo name
    if (extension) { // verificar si se encontró el elemento
        elem3.setAttribute('value', extension); // establecer el valor del elemento usando setAttribute
        // o bien, puedes asignar el valor a la propiedad "value" del elemento:
        // elem2.value = "ejemplo";
        console.log('valor del elemento:', elem3.getAttribute('value')); // acceder al valor del elemento usando getAttribute
    } else {
        console.log('No se encontró el elemento');
        fileName = undefined;
    }
}


function escribirdos() {
    console.log('escribirdos');
    console.log('extfinal:', extension);
    console.log('nombre:', fileName);
    var elem2 = document.querySelector('input[name="muar_tipo"]'); // buscar el elemento por su atributo name
    if (extension) { // verificar si se encontró el elemento
        elem2.setAttribute('value', tipo_arch); // establecer el valor del elemento usando setAttribute
        // o bien, puedes asignar el valor a la propiedad "value" del elemento:
        // elem2.value = "ejemplo";
        console.log('valor del elemento:', elem2.getAttribute('value')); // acceder al valor del elemento usando getAttribute
    } else {
        console.log('No se encontró el elemento');
        fileName = undefined;
    }
}


function escribir() {
    console.log('estoysubiendounarchivo');
    uploadObj = new ej.inputs.Uploader({
        asyncSettings: {
            saveUrl: '/500/upload_file/',
            removeUrl: '/500/delete_file/',
            autoUpload: false // deshabilitar la subida automática
        },
        //para que funcionen los metodos onupload
        success: onUploadSuccess,
        failure: onUploadFailure,
        removing: onFileRemove // agregar el evento de eliminación
    });
    uploadObj.appendTo(elem);

    function onUploadSuccess(args) {
        if (args.operation === 'upload') {
            var file = args.file.rawFile;
            var reader = new FileReader();
            var variable = file.type;
            var variable2 = file.name;
            var resultado = variable.split('/')[0];
            var resultado2 = variable.split('/')[1];
            console.log('........... pelao ' + resultado);
            console.log('........... imagen ' + variable2);

            reader.readAsDataURL(file);
            reader.onload = function () {
                var fileData = reader.result;
                var now = new Date();
                var fechaHoraActual = now.getFullYear() + '-' + (now.getMonth()) + '-' + now.getDate() + ' ' + now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();

                fechaHoraActual = fechaHoraActual.replace(/:/g, '-');
                fechaHoraActual = fechaHoraActual.replace(/ /g, '_');
                console.log('ESTOYHARTOOOOOO,FECHACTUAL ', fechaHoraActual);
                var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
                console.log('nombrearchivo: ', file.name);
                var response = args.e.currentTarget.response;
                var jsonResponse = JSON.parse(response);

                console.log("JSON ",jsonResponse)

                var url = jsonResponse.url;
                console.log('url', url);
                // fileName = url;
                ruta_archivo = url;
                console.log('nombrearchivop: ', fileName);

                const partes = url.split("/"); // dividir la URL por "/"
                extension = ruta_archivo.split('.').pop();
                //Define un objeto que mapea las extensiones de archivo a tipos de archivo
                // var tiposArchivo = {
                //     "jpg": 'Imagen',
                //     "jpeg": 'Imagen',
                //     "jpe": 'Imagen',
                //     "jif": 'Imagen',
                //     "jfif": 'Imagen',
                //     "jfi": 'Imagen',
                //     "png": 'Imagen',
                //     "gif": 'Imagen',
                //     "bmp": 'Imagen',
                //     "webp": 'Imagen',
                //     "tiff": 'Imagen',
                //     "tif": 'Imagen',
                //     "svg": 'Imagen',
                //     "mp3": 'Audio',
                //     "wav": 'Audio',
                //     "aiff": 'Audio',
                //     "m4a": 'Audio',
                //     "aif": 'Audio',
                //     "flac": 'Audio',
                //     "ogg": 'Audio',
                //     "mp4": 'Video',
                //     "mov": 'Video',
                //     "avi": 'Video',
                //     "wmv": 'Video',
                //     "mkv": 'Video',
                //     "mpeg": 'Video',
                //     "mpg": 'Video',
                //     "webm": 'Video',
                //     "flv": 'Video',
                //     "pdf": 'Documento',
                //     "doc": 'Documento',
                //     "docx": 'Documento',
                //     "xls": 'Documento',
                //     "xlsx": 'Documento',
                //     "ppt": 'Documento',
                //     "pptx": 'Documento',
                //     "txt": 'Documento',
                //     "rtf": 'Documento',
                //     "zip": 'Archivo comprimido',
                //     "rar": 'Archivo comprimido',
                //     "tar": 'Archivo comprimido',
                //     "7z": 'Archivo comprimido',
                //     "gz": 'Archivo comprimido',
                //     "bz2": 'Archivo comprimido'
                // };
                // var tiposArchivo = {
                //     "image": 'Imagen',
                //     "video": 'Video',
                //     "audio": 'Audiox',
                //     "document": 'Documentox'
                // };

                //Obtén el tipo de archivo a partir de la extensión
                var tipoArchivo = resultado;
                tipo_arch = tipoArchivo;
                formato_arch = "." + extension;
                //Imprime el tipo de archivo en la consola
                console.log("Tipo de archivo: " + tipoArchivo);
                console.log("Parteeeeeeees: " + partes[2]);
                fileName = partes[2];
                arreglo[contador]=fileName;
                contador=contador+1;
                console.log('EL URL PELAOOOO:', ruta_archivo, ' extension : ', extension);
                escribirdos();
                escribirtres();
                // $.ajax({
                //     type: "POST",
                //     url: '/200/upload_file/',
                //     headers: {
                //         'X-CSRFToken': csrfToken
                //     },
                //     data: {
                //         file_name: fileName,
                //         file_data: fileData
                //     },
                //     success: function(response) {
                //         console.log('archivoensuccessajax: ', fileName);
                //         console.log(response);
                //         console.log('pelao');
                //
                //         // console.log(uploaded_file_url);
                //         // ruta_archivo = response.uploaded_file_url;
                //         // console.log(ruta_archivo);
                //     },
                //     error: function(error) {
                //         console.log('fuenomas');
                //         console.log(error);
                //     }
                // });
            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
        }
    }

    function onUploadFailure(args) {
        console.log('File failed to upload');
    }
}

function onFileRemove(args) {

    // obtener la URL del archivo
    var fileUrl = ruta_archivo;

    console.log('ESTOY HACIENDO LA ELIMINACION ', fileUrl);
    console.log('QUERECIBOOOOOOOOOOOOOOO¿?: ', fileName);
    // enviar una solicitud para eliminar el archivo
    //  if (confirm("¿Estás seguro de que deseas eliminar el archivo " + fileName + "?")) {
    $.ajax({
        type: "POST",
        url: '/200/delete_file/',
        // headers: {
        //     'X-CSRFToken': csrfToken
        // },
        data: {
            file_url: fileName,
        },
        success: function (response) {
            console.log('SE ELIMINO ', fileName);


            // console.log(uploaded_file_url);
            // ruta_archivo = response.uploaded_file_url;
            // console.log(ruta_archivo);
        },
        error: function (error) {
            console.log('fuenomasgg');
            console.log(error);
        }
    });
    // } else {
    // console.log("La eliminación del archivo " + fileName + " fue cancelada.");
// }
}

function handleDeleteButtonClick(args) {
    console.log('botonborrargrilla');
    alert('test');
    // if (confirm("¿Estás seguro de que deseas eliminar el archivo " + fileName + "?")) {
    if (args.item.id === "multimedia_grid_delete") {
        // Obtener el objeto de la cuadrícula
        var gridObj = document.getElementById('multimedia_grid').ej2_instances[0];

        // Obtener la fila seleccionada
        var selectedRecords = gridObj.getSelectedRecords();

        // Comprobar si se ha seleccionado una fila
        if (selectedRecords.length > 0) {
            // Obtener los valores de muar_ruta y muar_tipo de la fila seleccionada
            var mulArchivo = selectedRecords[0].muar_ruta;
            var mulTipo = selectedRecords[0].muar_tipo;

            // Hacer lo que necesites con los valores
            console.log("Archivo: ", mulArchivo);
            console.log("Tipo: ", mulTipo);
            ruta_archivo = mulArchivo;
            var mulArchivoNombre = mulArchivo.split('/').pop();
            fileName = mulArchivoNombre;
            onFileRemove();
        }
    }
    // } else {
    // console.log("La eliminación del archivo " + fileName + " fue cancelada.");
// }
}



//
// function Save()
// {
//     try
//     {
//         if (HttpContext.Current.Request.Files.AllKeys.Length > 0)
//         {
//             var httpPostedFile = HttpContext.Current.Request.Files["UploadFiles"];
//
//             if (httpPostedFile != null)
//             {
//                 var fileSave = HttpContext.Current.Server.MapPath("UploadedFiles");
//                 var fileSavePath = Path.Combine(fileSave, httpPostedFile.FileName);
//                 if (!File.Exists(fileSavePath))
//                 {
//                     httpPostedFile.SaveAs(fileSavePath);
//                     HttpResponse Response = HttpContext.Current.Response;
//                     Response.Clear();
//                     Response.ContentType = "application/json; charset=utf-8";
//                     Response.StatusDescription = "File uploaded succesfully";
//                     Response.End();
//                 }
//                 else
//                 {
//                     HttpResponse Response = HttpContext.Current.Response;
//                     Response.Clear();
//                     Response.Status = "400 File already exists";
//                     Response.StatusCode = 400;
//                     Response.StatusDescription = "File already exists";
//                     Response.End();
//                 }
//             }
//         }
//     }
//     catch (Exception e)
//     {
//         HttpResponse Response = System.Web.HttpContext.Current.Response;
//         Response.Clear();
//         Response.ContentType = "application/json; charset=utf-8";
//         Response.StatusCode = 400;
//         Response.Status = "400 No Content";
//         Response.StatusDescription = e.Message;
//         Response.End();
//     }
// }
var elem
var strm
var ruta_archivo
var extension
var fileName
var tipo_arch
var formato_arch
var contador = 0
var arreglo = []
var Contador = 0
var Valor_Previo
// Cantidad
function crear() {

    console.log('CREAR EDITOR ENRIQUECIDO');

    // Crear un elemento textarea para el editor
    var textareaElem = document.createElement('textarea');
    textareaElem.setAttribute('name', 'myricheditor');

    // Asignar una clase para identificarlo
    textareaElem.classList.add('ckeditor');
    textareaElem.style.width = '100%'; // Ancho del editor
    textareaElem.style.minHeight = '300px'; // Altura mínima del editor

    // Inicializar CKEditor en el elemento textarea
    ClassicEditor
        .create(textareaElem, {
        })
         .then(editor => {
             editorInstance = editor; // Almacenar la instancia en la variable
             editorCreado();
        })
        .catch(error => {
            console.error(error);
        });
    elem = textareaElem
    // Devolver el elemento textarea con CKEditor inicializado

    return elem;
}


function leer() {
    console.log('LEER');
    strm = 'perxD';
    if (editorInstance) {
        // Obtener el contenido del editor a través de la instancia
        strm = editorInstance.getData();
        Valor_Previo = strm;
        var elem4 = document.querySelector('input[name="ind_descripcion_seguridad"]');
        elem4.setAttribute('value', strm);
    }

    return strm;
}

function leerdos() {
    console.log('LEERdos');
    strm = Valor_Previo;

    return strm;
}

function destruir() {
    console.log('DESTRUIR');
    // onFileRemove();
    extension = undefined;

}



function escribir() {
    console.log('escribir');
    var elem3 = document.querySelector('input[name="ind_descripcion_seguridad"]');
    // // var elem3 = document.querySelector('input[name="ind_nombre"]');
    Valor_Previo = elem3.value;
    // // var valorCampo = elem3.value;
    // console.log(valorCampo);
    // // elem3.setAttribute('value', 'zzzz');

}

function editorCreado() {
    // Llamar a la función escribir() aquí para asegurarse de que la instancia esté disponible
    if (editorInstance) {
        editorInstance.setData(Valor_Previo);
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
            // Obtener los valores de mul_archivo y mul_tipo de la fila seleccionada
            var mulArchivo = selectedRecords[0].mul_archivo;
            var mulTipo = selectedRecords[0].mul_tipo;

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
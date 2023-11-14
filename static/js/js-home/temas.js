$(document).ready(function() {
    // Función que manejará la petición AJAX
    function fetchTemas(asi_id, searchTerm) {
        $.ajax({
            url: '/../100/temas_por_asignatura/',
            type: 'GET',
            data: {
                'asi_id': asi_id,
                'searchTerm': searchTerm
            },
            dataType: 'json',
            success: function(data) {
                $('#temas').empty();
                data.forEach(function(tema) {
                     let opciones2 = `
            <div class="col-lg-4 col-md-6 mb-3">
              <div class="bg-light rounded-top w-100 h-50 mx-auto p-3">
                <img class="img-fluid rounded" style="width: 100%; height: 100%; object-fit: cover; object-position: center;" src="${tema.tema_imagen_url}" alt="">
              </div>
<div class="bg-light rounded-bottom p-4">
                                <div class="d-flex align-items-center justify-content-center description2">
                                    <span class="text-center fw-bold" style="font-size: calc(1.275rem + .3vw);font-family:cursive; color: #FE5D37">${tema.tem_nombre}</span>
                                </div>
                                <div>
                                    <p class="text-secondary description" style="text-align: justify; font-family: cursive">${tema.tem_descripcion}</p>
                                </div>
                              
                                 <div class="d-flex justify-content-between align-items-center my-2">
                                    <div>
                                       <div>
                                <span class="text-secondary" style="text-align: justify; font-family: cursive">Asignatura:</span>
                                <span class="text-warning">${tema.asi_nombre}</span>
                            </div>
                            <div>
                                <span class="text-secondary" style="text-align: justify; font-family: cursive">Nro. Actividades:</span>
                                <span class="text-success">${tema.numero_de_actividades}</span>
                            </div>
                                    </div>
                                    <div> <!-- Botón Comenzar -->
                                        <button class="btn btn-success startBtn px-4" data-parametro="${tema.tem_id}"
                                    style="text-align: justify; font-family: cursive">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                                     class="bi bi-play" viewBox="0 0 16 16">
                                    <path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"></path>
                                </svg>
                            </button>
                                    </div>
                                </div>
                            </div>
</div>`;
                    $('#temas').append(opciones2);
                });
            }
        });
    }

    // Al seleccionar una asignatura
    $('li[data-asi_id]').click(function() {
        var asi_id = $(this).data('asi_id');
        var searchTerm = $("#searchInput").val();
        fetchTemas(asi_id, searchTerm);
    });

    // Al ingresar texto en la barra de búsqueda
    $("#searchInput").on('input', function() {
        var searchTerm = $(this).val();
        var asi_id = $("li[data-asi_id].selected").data("asi_id");
        fetchTemas(asi_id, searchTerm);
    });

    // Al hacer clic en el botón de búsqueda
    $("#searchButton").click(function() {
        var searchTerm = $("#searchInput").val();
        var asi_id = $("li[data-asi_id].selected").data("asi_id");
        fetchTemas(asi_id, searchTerm);
    });
});

document.getElementById("temas").addEventListener("click", function(e) {
    // Si el elemento clicado o uno de sus ancestros es un .startBtn
    if (e.target.closest('.startBtn')) {
        const btn = e.target.closest('.startBtn');
        const tem_id = btn.getAttribute("data-parametro");
         const asi_id = btn.getAttribute("data-parametro2");
        window.location.href = "/../100/actividades/" + tem_id;
    }
});
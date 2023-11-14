    var respuestaCorrecta2 = "{% for respuesta in respuestas %}{% if respuesta.res_escorrecta %}{{ respuesta.res_respuesta }}{% endif %}{% endfor %}";
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
  ev.dataTransfer.setData("parameter", ev.target.getAttribute('data-parameter')); // store the parameter in the dataTransfer object
}
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var parameter = ev.dataTransfer.getData("parameter");
    var node = document.getElementById(data);
    node.parentNode.removeChild(node);
    ev.target.appendChild(node);
    $(document).trigger('elementoArrastrado', [parameter]);
}

   let opciones = ``;
function modModal(tem_id, tem_nombre){
var tema=document.getElementById('tit_modal')
    tema.innerHTML=tem_nombre;
}


const listarActividades = async (tem_id) => {
    opciones = ``;
  try {
    const response = await fetch(`http://127.0.0.1:8000/100/list_tact/${tem_id}`);
    const data = await response.json();

    if (data.message === "Success") {
      const temas = data.temas;

      for (const tema of temas) {
        const response2 = await fetch(`http://127.0.0.1:8000/100/list_act/${tema.act_id}`);
        const data2 = await response2.json();

        if (data2.message === "Success") {
          const actividades = data2.actividad;

          for (const actividad of actividades) {
              opciones+=`<li class="link-primary bg-white py-2 border-bottom border-secondary" data-parametro1="${tem_id}" data-parametro2="${tema.act_id}">${actividad.act_nombre}</li>`;
          }
          document.getElementById("lista-act").innerHTML=opciones;
        } else {
          alert("Tema-Actividad no encontrados...");
        }
      }
    } else {
      alert("Tema-Actividad no encontrados...");
    }
  } catch (error) {
    console.log(error);
  }
};

var div = document.getElementById('temas');
// Agregar un controlador de eventos al contenedor div
div.addEventListener('click', function(event) {
  // Verificar si se hizo clic en una etiqueta <a>
  if (event.target.tagName === 'A') {
    // Obtener el valor de la etiqueta <a> clicada
    var tem_id = event.target.getAttribute('value');
    var  tem_nombre= event.target.innerHTML;
    // Hacer algo con el valor de la etiqueta <a> clicada
    modModal(tem_id,tem_nombre);
    listarActividades(tem_id);
  }
});


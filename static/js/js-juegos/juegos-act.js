

  // // Script para capturar el clic en los botones "Jugar" individuales
  // document.querySelectorAll(".startBtn").forEach(function(btn) {
  //   btn.addEventListener("click", function() {
  //     const jueId = this.getAttribute("data-jue-id");
  //     const tipId = this.getAttribute("data-tip-id");
  //
  //     // Redireccionar a la URL con los datos de jue_id y tip_id como parámetros
  //     window.location.href = "/../100/tipo/" + tipId + "/" + jueId+"/";
  //   });
  // });
  // document.querySelectorAll(".startBtn").forEach(function(btn) {
  //   btn.addEventListener("click", function() {
  //     const juegos = [];
  //     const jueId = this.getAttribute("data-jue-id");
  //     const tipId = this.getAttribute("data-tip-id");
  //     juegos.push({ jue_id: jueId, tip_id: tipId });
  //     // Redireccionar a la URL con los datos de jue_id y tip_id como parámetros
  //     // window.location.href = "/../100/tipo/" + tipId + "/" + jueId+"/";
  //     const juegosJSON = encodeURIComponent(JSON.stringify(juegos));
  //     window.location.href = `/../100/tipos/${juegosJSON}/`;
  //   });
  // });

 document.getElementById("temas").addEventListener("click", function(e) {
    // Si el elemento clicado o uno de sus ancestros es un .startBtn
    if (e.target.closest('.startBtn')) {
       const juegos = [];
       const btn = e.target.closest('.startBtn');
      const jueId = btn.getAttribute("data-jue-id");
      const tipId = btn.getAttribute("data-tip-id");
      juegos.push({ jue_id: jueId, tip_id: tipId });
      // Redireccionar a la URL con los datos de jue_id y tip_id como parámetros
      // window.location.href = "/../100/tipo/" + tipId + "/" + jueId+"/";
      const juegosJSON = encodeURIComponent(JSON.stringify(juegos));
      window.location.href = `/../100/tipos/${juegosJSON}/`;
    }
});
// Script para capturar el clic en el botón "Jugar Todos"
  document.getElementById("jugarTodosBtn").addEventListener("click", function() {
    // Obtener todos los botones "Jugar" individuales
    const jugarBtns = document.querySelectorAll(".startBtn");

    // Obtener los datos de jue_id y tip_id de cada fila y almacenarlos en una lista
    const juegos = [];
    jugarBtns.forEach(function(btn) {
      const jueId = btn.getAttribute("data-jue-id");
      const tipId = btn.getAttribute("data-tip-id");
      juegos.push({ jue_id: jueId, tip_id: tipId });
    });

    // Convertir la lista de juegos a una cadena JSON y codificarla para enviarla como parámetro en la URL
    const juegosJSON = encodeURIComponent(JSON.stringify(juegos));
window.location.href = `/../100/tipos/${juegosJSON}/`;
  });
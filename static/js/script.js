/* Autores: Bryan Amaya */
// preguntas[0] =
//         {
//             titulo: [enunciado[0]],
//             alternativas: [a[0]],
//             correcta: [1]
//         }
// for (let registro in a) {
//     // console.log(a[registro],b[registro]);
//     // console.log(preguntas[0].correcta[0]);
//     if (b[registro]=='True'){
//             preguntas[0].correcta[0] = registro;
//         }
//     preguntas[0].alternativas[registro] = a[registro];
// }


// console.log(preguntas[0], 'gg');
// console.log(JSON.stringify(preguntas[0]),'ggJSON');
// // console.log(preguntas[1], 'gg')
// let preguntas2 = [
//     {
//         titulo: "Uma",
//         alternativas: ["Cabeza", "Mano", "Cuello", "Brazo"],
//         correcta: "Cabeza"
//     },
//     {
//         titulo: "Chaki",
//         alternativas: ["Pie", "Pierna", "Oreja", "Ojo"],
//         correcta: "Pie"
//     },
//     {
//         titulo: "Sinqa",
//         alternativas: ["Boca", "Oreja", "Lengua", "Nariz"],
//         correcta: "Lengua"
//     },
// ]
// console.log(preguntas2[0], 'gg2');
// var a = JSON.parse(document.getElementById('namer').textContent);
// console.log(a);

    function display_image(src, width, height, alt) {
    var a = document.createElement("img");
    a.src = src;
    a.width = width;
    a.height = height;
    a.alt = alt;
    document.body.appendChild(a);
    }

var hola = "";
let app = {

    start: function () {

        this.PosActual = 0;
        this.Totalpuntos = 0;
        // console.log("testF",preguntas[this.PosActual].alternativas.length);

        // document.write("<div id='wrapper'>")
        // document.write("<ul>");
        let text = "";
        for (let i = 0; i < preguntas[this.PosActual].alternativas.length; i++) {
            // document.write("<li class='alternativa'></li>");
            text += "<li class='alternativa'></li>";
        }
        document.getElementById("opciones").innerHTML = text;
        let alts = document.querySelectorAll('.alternativa');
        alts.forEach((element, index) => {
            element.addEventListener('click', () => {
                // console.log("RESPESCUCHADA");
                this.checaRespuesta(index);
            })
        })
        this.actualizaPuntos();
        app.muestrapalabra(preguntas[this.PosActual]);
    },

    muestrapalabra: function (q) {

        console.log("Puntaje Pregunta Actual ", puntaje[this.PosActual]);
        // document.write("</ul>");
        // document.write("</div>");
        this.qatual = q;
        let page=document.getElementById("page");
        page.innerText=this.PosActual+"/"+preguntas.length;
        console.log("QUE ES ESTO " ,this.PosActual);
        // mostrando o titulo
        let titleDiv = document.getElementById('titulo');
        titleDiv.textContent = q.titulo;
        // mostrando as alternativas
        let alts = document.querySelectorAll('.alternativa');
        alts.forEach(function(element,index){
            element.textContent = q.alternativas[index];
            // console.log(q,element.textContent,'REIMPORTANTE')
        })
        this.actualizaPuntos();

    
    },

    siguientePregunta: function () {
        this.PosActual++;
        console.log("HOLA ", this.PosActual);
        if (this.PosActual == preguntas.length) {
            // this.PosActual = 0;
            console.log("ENTRE ", this.PosActual);
            Swal.fire({
                title: 'Juego completado!, Puntuación obtenida: ' + this.Totalpuntos + '/' + TotalPuntJuego,
                showDenyButton: true,
                showCancelButton: true,
                confirmButtonText: 'Enviar resultados',
                denyButtonText: `No Enviar resultados`,
                cancelButtonText: `Repetir Juego`,
            }).then((result) => {
                /* Read more about isConfirmed, isDenied below */
                if (result.isConfirmed) {
                    Swal.fire('Resultados enviados!, regresando a la pagina principal...', '', 'success')
                    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
                    const pagPrincipal = async () => {
                        await sleep(3000)
                        location.replace("http://127.0.0.1:8000/400/temas/")
                    }
                    pagPrincipal()

                } else if (result.isDenied) {
                    Swal.fire('Resultados no enviados!', '', 'info')
                } else {
                    let resultDiv = document.getElementById('result');
                    this.PosActual = 0;
                    this.Totalpuntos = 0;
                    Swal.fire('Repitiendo juego!', '', 'info')
                    result = ``;
                    resultDiv.textContent = result;
                    var correcto = document.getElementById("imagencorrecto");
                    correcto.innerHTML="";
                    var incorrecto = document.getElementById("imagenincorrecto");
                    incorrecto.innerHTML="";
                    this.actualizaPuntos();
                    this.muestrapalabra(preguntas[this.PosActual]);

                }
            })
        }
    },

    checaRespuesta: function (user) {
        let pregunta = preguntas[this.PosActual];
        let ctexto = pregunta.alternativas[user];
        console.log(`${ctexto}`)
        if (this.qatual.correcta == `${ctexto}`) {
            console.log(user)
            this.Totalpuntos= this.Totalpuntos+parseFloat(puntaje[this.PosActual].replace(/,/g, '.'));
            this.mostrarespuesta(true);
            this.siguientePregunta();
        } else {
            let pregunta = preguntas[this.PosActual];
            let ctexto = pregunta.alternativas[user];
            console.log(`${ctexto}`)
            console.log(user)
            console.log("Incorrecta")
            this.mostrarespuesta(false);
        }
        this.actualizaPuntos();
        this.muestrapalabra(preguntas[this.PosActual]);
    },
    
    actualizaPuntos: function(){
        let scoreDiv = document.getElementById('puntos');
        scoreDiv.textContent = `Su Puntuación: ${this.Totalpuntos}`;
    },
    mostrarespuesta: function (correto) {
        let resultDiv = document.getElementById('result');
        let result = '';
        // formate a mensagem a ser exibida
        if (correto) {
            result = 'Respuesta Correcta!';
            var correcto = document.getElementById("imagencorrecto");
            correcto.innerHTML="<img src=\"/static/img/carafeli2.png\" width=\"400px\" height=\"150px\">";
            var incorrecto = document.getElementById("imagenincorrecto");
            incorrecto.innerHTML="";
            backgroundColor = 'red';
        } else {
            // // obtenha a questão atual
            // let pregunta = preguntas[this.PosActual];
            // // obtenha o índice da respuesta correcta da questão atual
            // let cindice = pregunta.correcta;
            // // obtenha o texto da respuesta correcta da questão atual
            // let ctexto = pregunta.alternativas[cindice];
            let pregunta = preguntas[this.PosActual];
            let poscorrecto = -1;
            for (let registro in pregunta.alternativas) {
                console.log('HURRA', registro);
                console.log('HURRA2', pregunta.alternativas[registro]);
                console.log('HURRA3', pregunta.correcta);
                if (pregunta.alternativas[registro] == pregunta.correcta) {
                    console.log('HURRAF', registro);
                    poscorrecto = registro;
                    break;
                }

            }
            let ctexto = pregunta.alternativas[poscorrecto];

            result = `Incorrecto! Respuesta Correcta: ${ctexto}`;
            var correcto = document.getElementById("imagencorrecto");
            correcto.innerHTML="";
            var incorrecto = document.getElementById("imagenincorrecto");
            incorrecto.innerHTML="<img src=\"/static/img/intentalo.png\" width=\"400px\" height=\"150px\">";
        }
        resultDiv.textContent = result;
        
      }


    }

    app.start();


// Ventana modal
var modal = document.getElementById("ventanaModal");

// Botón que abre el modal
var boton = document.getElementById("abrirModal");

// Hace referencia al elemento <span> que tiene la X que cierra la ventana
var span = document.getElementsByClassName("cerrar")[0];

// Cuando el usuario hace click en el botón, se abre la ventana
boton.addEventListener("click",function() {
  modal.style.display = "block";
});

// Si el usuario hace click en la x, la ventana se cierra
span.addEventListener("click",function() {
  modal.style.display = "none";
});

// Si el usuario hace click fuera de la ventana, se cierra.
window.addEventListener("click",function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
});
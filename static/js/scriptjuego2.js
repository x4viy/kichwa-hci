// Autor: Bryan Amaya
var totalCorrectas=0;
var totalSeleccionadas=0;
var preguntaActual=0;
var Totalpuntos = 0;
// var preguntas=[
//     {
//         "titulo":["Papa en Quechua es "," significa Papá"],       // titulo
//         "alternativas":["Machula","Tayta","Wawqi","Tura","Kaki"],// alternativas
//         "correcta":["Tayta"]                                // correcta
//     },
//     {
//         "titulo":["Mamá: ",""],
//         "alternativas":["Wawqi","Payala","Mama","Sispa tura","Tayta"],
//         "correcta":["Mama"]
//
//     },
//     {
//         "titulo":["Tía: ",""],
//         "alternativas":["Mama","Tura","Ipa","Machula","Wawqi"],
//         "correcta":["Ipa"]
//
//     },
//     {
//         "titulo":["Sobrino: ",""],
//         "alternativas":["Tayta","Mama","Ipa","Kaki","Mulla"],
//         "correcta":["Mulla"]
//
//     },
//     {
//         "titulo":["Hermana: ",""],
//         "alternativas":["Machula","Sispa tura","Ñaña","Payala"],
//         "correcta":["Ñaña"]
//
//     }
// ]

function cargarPregunta(){
    this.actualizaPuntos();
    let page=document.getElementById("page");
    page.innerText=`${preguntaActual+1}/${preguntas.length}`;
    let palabras=document.getElementById("palabras");
    palabras.innerText="";
    for(let j=0;j<preguntas[preguntaActual].alternativas.length;j++){
        let option=document.createElement('div');
        option.className="palabra";
        option.draggable=true;
        option.id=`option${preguntaActual}${j}`;
        option.innerText=preguntas[preguntaActual].alternativas[j];
        option.ondragstart=event=>{
            event.dataTransfer.setData("id", event.target.id);
            console.log("Drag started");

        }

        palabras.appendChild(option);
    }

        let q=document.getElementById("titulo");
        q.innerText="";
        let fieldNumber=0;
        for(let j=0;j<preguntas[preguntaActual].titulo.length;j++){
            q.innerHTML+=preguntas[preguntaActual].titulo[j];
            console.log(preguntas[preguntaActual].titulo[j].slice(-1));

            const field=document.createElement('span');
            field.className="field";
            field.id=`field${preguntaActual}${fieldNumber}`;
            fieldNumber++;
            q.append(field);

            
        }

    var fields = document.getElementsByClassName("field");
    for (var i = 0; i < fields.length; i++) {
        fields[i].addEventListener('dragover', event=>{
            let submitErroneo=document.getElementById('submit');
            submitErroneo.className="boton-incognita";
            event.preventDefault();
        }, false);
        fields[i].addEventListener("drop",e=>drop(e),false);
        fields[i].addEventListener("dblclick",e=>{

            e.target.className="field";
            e.target.innerText="";
            // e.target.style.backgroundColor="#c7c7c7";
        },false);
    }
}

function drop(e) {
    var data = e.dataTransfer.getData("id");
    const seleccion=document.getElementById(data);
    e.target.innerText=seleccion.innerText;
    e.target.className="palabra";
}

function siguientePregunta(){

    let primeraSeleccion=document.getElementById(`field${preguntaActual}0`);
    if(primeraSeleccion.innerText!==""){
        //fields are not empty
        let primeraRespuesta=preguntas[preguntaActual].correcta[0];

        if(primeraRespuesta===primeraSeleccion.innerText){
            console.log("soy feliz", preguntaActual);
            this.Totalpuntos= this.Totalpuntos+parseFloat(puntaje[this.preguntaActual].replace(/,/g, '.'));
            totalCorrectas+=2;
            totalSeleccionadas+=2;
            var correcto = document.getElementById("imagencorrecto");
            correcto.innerHTML="<img src=\"/static/img/carafeli2.png\" width=\"400px\" height=\"150px\">";
            var incorrecto = document.getElementById("imagenincorrecto");
            incorrecto.innerHTML="";
            preguntaActual++;

            this.actualizaPuntos();
            if(preguntaActual===preguntas.length){

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
                    this.preguntaActual = 0;
                    this.Totalpuntos = 0;
                    Swal.fire('Repitiendo juego!', '', 'info')
                    var correcto = document.getElementById("imagencorrecto");
                    correcto.innerHTML="";
                    var incorrecto = document.getElementById("imagenincorrecto");
                    incorrecto.innerHTML="";
                    this.actualizaPuntos();
                    this.cargarPregunta();

                }
            })

            }
            else cargarPregunta();

        }
        else{
            //alternativas are wrong
            if(primeraRespuesta!==primeraSeleccion.innerText){
                primeraSeleccion.className="palabra respuesta-incorrecta";
                let submitErroneo=document.getElementById('submit');
                submitErroneo.className="boton-incorrecta";
                var correcto = document.getElementById("imagencorrecto");
                correcto.innerHTML="";
                var incorrecto = document.getElementById("imagenincorrecto");
                incorrecto.innerHTML="<img src=\"/static/img/intentalo.png\" width=\"400px\" height=\"150px\">";
                totalSeleccionadas+=1;
            }
        }
        
    }
    else{
        alert("Debes completar espacios vacios");
    }
    
}

function loadResult(right,total){
    document.getElementById("logo").src="";
    let mensaje=document.getElementById("mensaje");
    let palabras=document.getElementById("palabras");
    let titulo=document.getElementById("titulo");
    let percent=right/total*100;
    if(percent>=90){
        document.getElementById("logo").src="https://www.clipartmax.com/png/full/335-3351566_super-duo-duolingo.png";
        titulo.innerText="Congrats! You're a champion!";
    }
    else if(percent>=50){
        document.getElementById("logo").src="https://www.clipartmax.com/png/full/270-2701318_see-4th-of-july-language-exchange-at-duolingo-medell%C3%ADn-duolingo-italian.png";
        titulo.innerText="You've done great.";
    }
    else{
        document.getElementById("logo").src="https://www.clipartmax.com/png/full/110-1106414_duolingo-crying-owl.png";
        titulo.innerText="Try harder next time.";
    }
    mensaje.style.display="none";
    palabras.style.display="none";
    document.getElementById("submit").style.display="none";
    document.getElementById("title").innerText=`${right}/${totalSeleccionadas} Palabras Correctas`;    
}

function actualizaPuntos(){
        let scoreDiv = document.getElementById('puntos');
        scoreDiv.textContent = `Su Puntuación: ${this.Totalpuntos}`;
    }






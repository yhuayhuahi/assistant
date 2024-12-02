<template>
    <div>
      <button @click="irAAsistente">Ir al Asistente Psicológico</button>
      <h1>Control del Micrófono</h1>
      <button @click="toggleMic">{{ isMicOn ? 'Apagar Micrófono' : 'Encender Micrófono' }}</button>
      <p>Estado: {{ micStatus }}</p>
  
      <div v-if="mensaje" class="message-box">
        <h2>Mensaje del Usuario:</h2>
        <p>{{ mensaje }}</p>
      </div>
  
      <button v-if="mensaje" @click="enviarMensaje">Enviar</button>
  
      <div v-if="respuesta" class="response-box">
        <h2>Respuesta del Asistente:</h2>
        <p>{{ respuesta }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Asegúrate de importar axios
  
  export default {
    data() {
      return {
        mensaje: "",
        respuesta: "",
        reconocimiento: null,
        micStatus: "Micrófono apagado",
        isMicOn: false,
      };
    },
    methods: {
      irAAsistente() {
        this.$router.push('/asistente-psicologico');
      },
      iniciarVoz() {
        if (!("webkitSpeechRecognition" in window)) {
          alert("Tu navegador no soporta reconocimiento de voz.");
          return;
        }
  
        // Si ya existe una instancia, detenemos y reiniciamos
        if (this.reconocimiento) {
          this.reconocimiento.stop();
          this.reconocimiento = null;
        }
  
        this.reconocimiento = new webkitSpeechRecognition();
        this.reconocimiento.continuous = true;
        this.reconocimiento.lang = "es-ES";
        this.reconocimiento.interimResults = false;
  
        this.reconocimiento.onresult = (event) => {
          const texto = event.results[event.results.length - 1][0].transcript;
          this.mensaje = texto;
        };
  
        this.reconocimiento.onerror = (event) => {
          console.error("Error de reconocimiento: ", event.error);
        };
  
        this.reconocimiento.onend = () => {
          if (this.isMicOn) {
            this.reconocimiento.start(); // Reiniciar el reconocimiento si el micrófono está encendido
          }
        };
  
        this.reconocimiento.start();
        this.micStatus = "Escuchando...";
      },
      detenerVoz() {
        if (this.reconocimiento) {
          this.reconocimiento.stop();
          this.micStatus = "Micrófono apagado";
        }
      },
      toggleMic() {
        this.isMicOn = !this.isMicOn;
        this.micStatus = this.isMicOn ? "Micrófono encendido" : "Micrófono apagado";
        if (this.isMicOn) {
          this.iniciarVoz();
        } else {
          this.detenerVoz();
        }
      },
      async enviarMensaje() {
        try {
          if (this.mensaje.toLowerCase().includes("chiste")) {
            const response = await axios.get("http://localhost:8000/api/chiste/");
            this.respuesta = response.data?.chiste || "No encontré un chiste en este momento.";
            this.hablar(this.respuesta);
            return;
          }
  
          const response = await axios.post("http://localhost:8000/api/front/", {
            mensaje: this.mensaje,
          });
  
          this.respuesta = response.data?.message || "No hubo respuesta.";
          this.hablar(this.respuesta);
        } catch (error) {
          console.error(error);
          this.respuesta = "Error al procesar tu solicitud.";
          this.hablar(this.respuesta);
        }
      },
      hablar(texto) {
        if ("speechSynthesis" in window) {
          window.speechSynthesis.cancel();
  
          const maxLength = 200;
          const speechArray = texto.match(new RegExp(`.{1,${maxLength}}`, "g")) || [texto];
  
          speechArray.forEach((fragment, index) => {
            const speech = new SpeechSynthesisUtterance(fragment);
            speech.lang = "es-ES";
            speech.pitch = 1;
            speech.rate = 0.9;
            speech.volume = 1;
  
            if (index === speechArray.length - 1) {
              speech.onend = () => console.log("Voz terminada.");
            }
  
            speech.onerror = (e) => console.error("Error en síntesis:", e);
  
            window.speechSynthesis.speak(speech);
          });
        } else {
          alert("Tu navegador no soporta síntesis de voz.");
        }
      },
    },
  };
  </script>
  
<template>
  <div id="app">
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
    <router-link to="/asistente">
      <button>Asistente de Ayuda Psicológica</button>
    </router-link>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mensaje: "",
      respuesta: "",
      reconocimiento: null,
      micStatus: "Micrófono apagado",
      isMicOn: false
    };
  },
  methods: {
    iniciarVoz() {
      if (!("webkitSpeechRecognition" in window)) {
        alert("Tu navegador no soporta reconocimiento de voz.");
        return;
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

      this.reconocimiento.start();
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
        // Llamar al backend para obtener un chiste
        const response = await axios.get("http://localhost:8000/api/chiste/");

        if (response.data && response.data.chiste) {
          this.respuesta = response.data.chiste;
          this.hablar(this.respuesta);
        } else {
          this.respuesta = "Lo siento, no pude encontrar un chiste en este momento.";
          this.hablar(this.respuesta);
        }
        return;
      }

      const response = await axios.post("http://localhost:8000/api/front/", {
        mensaje: this.mensaje,
      });

      if (response.data.message) {
        this.respuesta = response.data.message;
        this.hablar(this.respuesta); // El asistente responde con voz
      } else if (response.data.error) {
        this.respuesta = `Error: ${response.data.error}`;
        this.hablar(this.respuesta);
      }
    } catch (error) {
      console.error(error);
      this.respuesta = "Hubo un error al procesar tu solicitud.";
      this.hablar(this.respuesta);
    }
  },
    hablar(texto) {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();

        // Dividir el texto en fragmentos pequeños
        const maxLength = 200; // Máximo de caracteres por fragmento
        const speechArray = texto.match(new RegExp(`.{1,${maxLength}}`, "g")) || [texto];

        speechArray.forEach((fragment, index) => {
          const speech = new SpeechSynthesisUtterance(fragment);
          speech.lang = "es-ES"; // Idioma español
          speech.pitch = 1; // Tono normal
          speech.rate = 0.9; // Velocidad un poco más lenta
          speech.volume = 1; // Volumen máximo

          // Si es el último fragmento, muestra mensaje de fin
          if (index === speechArray.length - 1) {
            speech.onend = () => console.log("Voz del asistente terminada.");
          }

          speech.onerror = (e) => console.error("Error en síntesis de voz:", e);

          // Reproducir el texto fragmentado
          window.speechSynthesis.speak(speech);
        });
      } else {
        alert("Tu navegador no soporta la síntesis de voz.");
      }
    }
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 80%;
  max-width: 900px;
  height: 100%;
  background: linear-gradient(90deg, #ff007f, #7f00ff);
  border: 5px solid #ff007f;
  border-radius: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  padding: 20px;
  color: white;
  text-align: center;
  margin: 20px auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #ffeb3b;
}

button {
  background: linear-gradient(45deg, #00ff7f, #00e5ff);
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-size: 1.2rem;
  cursor: pointer;
  margin: 10px 0;
  transition: transform 0.3s ease, background 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

button:hover {
  background: linear-gradient(45deg, #ff007f, #ff4500);
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

button[v-if="mensaje"] {
  background: linear-gradient(45deg, #ff5722, #ff9100);
}

button[v-if="mensaje"]:hover {
  background: linear-gradient(45deg, #ff6a00, #e65100);
}

.message-box, .response-box {
  background: linear-gradient(45deg, #ff00ff, #8000ff);
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
  text-align: left;
  width: 85%;
  max-width: 700px;
  color: white;
  font-size: 1.2rem;
  font-weight: 500;
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 30px;
}

.message-box h2, .response-box h2 {
  margin-bottom: 12px;
  font-size: 1.5rem;
  color: #fff700;
  text-transform: uppercase;
}

.message-box p, .response-box p {
  color: #e0e0e0;
  font-size: 1.1rem;
}

.message-box, .response-box {
  max-height: none; 
  overflow: visible;
}

</style>

<template>
  <div class="asistente-container">
    <h2>Asistente de Ayuda Psicológica</h2>

    <!-- Botón para activar o desactivar el micrófono -->
    <button @click="toggleMic">{{ isMicOn ? 'Apagar Micrófono' : 'Activar Micrófono' }}</button>

    <!-- Mostrar el mensaje capturado por el micrófono antes de enviarlo -->
    <div v-if="mensajeCapturado">
      <h3>Mensaje Capturado:</h3>
      <p>{{ mensajeCapturado }}</p>

      <!-- Botón para enviar el mensaje capturado al backend -->
      <button @click="enviarMensaje(mensajeCapturado)">Enviar al Asistente</button>
    </div>
    <div v-if="cargando" class="loading-box">
      <p>Cargando solicitud...</p>
    </div>
    <!-- Mostrar la respuesta del asistente -->
    <div v-if="respuesta">
      <button @click="detenerVozAsistente" :disabled="!isSpeaking">Detener Voz</button>
      <h3>Respuesta del Asistente:</h3>
      <p>{{ respuesta }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      mensajeCapturado: '', // Mensaje que el usuario dice antes de enviarlo
      respuesta: '', // Respuesta del asistente
      reconocimiento: null, // Instancia de reconocimiento de voz
      micStatus: 'Micrófono apagado', // Estado del micrófono
      isMicOn: false, // Estado del micrófono (encendido o apagado)
      isSpeaking: false, // Variable para saber si el asistente está hablando
      cargando: false,
    };
  },
  computed: {
  micStatusStyle() {
    return {
      color: this.isMicOn ? '#ff7043' : '#d32f2f',
      fontWeight: 'bold', 
    };
  }
},
  methods: {
    // Iniciar o continuar el reconocimiento de voz
    iniciarVoz() {
      if (!('webkitSpeechRecognition' in window)) {
        alert('Tu navegador no soporta reconocimiento de voz.');
        return;
      }

      if (this.reconocimiento) {
        this.reconocimiento.stop();  // Detener si ya está activo
        this.reconocimiento = null;  // Reiniciar la instancia de reconocimiento
      }

      this.reconocimiento = new webkitSpeechRecognition();
      this.reconocimiento.continuous = true;  // Mantener el micrófono encendido
      this.reconocimiento.lang = 'es-ES';
      this.reconocimiento.interimResults = false;
      this.reconocimiento.onresult = (event) => {
        const texto = event.results[0][0].transcript;
        this.mensajeCapturado = texto;  // Mostrar el mensaje capturado
      };

      this.reconocimiento.onerror = (event) => {
        console.error('Error de reconocimiento: ', event.error);
        this.detenerVoz();
      };

      this.reconocimiento.onend = () => {
        if (this.isMicOn) {
          this.reconocimiento.start();  // Reiniciar el reconocimiento si se detiene.
        }
      };

      this.reconocimiento.start();
      this.micStatus = 'Escuchando...';
    },

    // Detener reconocimiento de voz
    detenerVoz() {
      if (this.reconocimiento) {
        this.reconocimiento.stop();
        this.micStatus = 'Micrófono apagado';
        this.isMicOn = false;
      }
    },

    // Alternar el estado del micrófono
    toggleMic() {
      this.isMicOn = !this.isMicOn;
      if (this.isMicOn) {
        this.iniciarVoz();
      } else {
        this.detenerVoz();
      }
    },

    // Enviar mensaje al backend
    async enviarMensaje(mensaje) {
      this.cargando = true;
      if (!mensaje.trim()) return;  // No enviar si el mensaje está vacío

      try {
        const response = await axios.post('http://localhost:8000/api/assistant/', {
          mensaje: mensaje,
        });

        this.respuesta = response.data.message;
        this.hablar(this.respuesta);  // Hablar la respuesta del asistente
      } catch (error) {
        console.error('Error al comunicarse con el asistente:', error);
        this.respuesta = 'Ocurrió un error. Por favor, inténtalo de nuevo.';
        this.hablar(this.respuesta);
      } finally {
        this.cargando = false; // Ocultar caja de carga
      }
    },

    // Función para hablar el texto con la síntesis de voz
    hablar(texto) {
  if ("speechSynthesis" in window) {
    // Cancelamos cualquier síntesis de voz en curso
    window.speechSynthesis.cancel();

    // Dividimos el texto en fragmentos más pequeños
    const maxLength = 200;
    const speechArray = texto.match(new RegExp(`.{1,${maxLength}}`, "g")) || [texto];

    let index = 0;

    const speakNext = () => {
      if (index < speechArray.length) {
        const speech = new SpeechSynthesisUtterance(speechArray[index]);
        speech.lang = "es-ES";
        speech.pitch = 1;
        speech.rate = 0.9;
        speech.volume = 1;

        speech.onend = () => {
          index++;
          speakNext(); // Hablar el siguiente fragmento
        };

        speech.onerror = (e) => {
          console.error("Error en síntesis:", e);
        };

        window.speechSynthesis.speak(speech);
      }
    };

    speakNext(); // Iniciar el habla con el primer fragmento
  } else {
    alert("Tu navegador no soporta síntesis de voz.");
  }
},
    // Detener cualquier síntesis de voz en curso
    detenerVozAsistente() {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
        this.isSpeaking = false;
      }
    },
  },
};
</script>

<style scoped>
.asistente-container {
  padding: 20px;
  text-align: center;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

h3 {
  margin-top: 20px;
}

p {
  font-size: 18px;
  color: white;
  text-align: center;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>

<template>
  <div class="asistente-container">
    <h2>Asistente Psicológico</h2>

    <!-- Botón para activar o desactivar el micrófono -->
    <button @click="toggleMic">{{ isMicOn ? 'Apagar Micrófono' : 'Activar Micrófono' }}</button>

    <!-- Mostrar el mensaje capturado por el micrófono antes de enviarlo -->
    <div v-if="mensajeCapturado">
      <h3>Mensaje Capturado:</h3>
      <p>{{ mensajeCapturado }}</p>

      <!-- Botón para enviar el mensaje capturado al backend -->
      <button @click="enviarMensaje(mensajeCapturado)">Enviar al Asistente</button>
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
      isMicOn: false, // Estado del micrófono (encendido/apagado)
      isSpeaking: false, // Flag para saber si el asistente está hablando
    };
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
      this.reconocimiento.interimResults = false;  // No mostrar resultados intermedios
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
      }
    },

    // Función para hablar el texto con la síntesis de voz
    hablar(texto) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();  // Cancelar cualquier síntesis anterior

        const fragmentos = this.dividirTextoEnFragmentos(texto);

        this.isSpeaking = true;

        fragmentos.forEach((fragmento, index) => {
          const utterance = new SpeechSynthesisUtterance(fragmento);
          utterance.lang = 'es-ES';
          utterance.pitch = 1;
          utterance.rate = 0.9;
          utterance.volume = 1;

          // Evento cuando termina de hablar
          utterance.onend = () => {
            if (index === fragmentos.length - 1) {
              console.log('Síntesis de voz completada.');
              this.isSpeaking = false;  // Ya terminó de hablar
            }
          };

          // Manejo de errores
          utterance.onerror = (e) => {
            console.error('Error en síntesis de voz:', e.error);
            this.isSpeaking = false;
          };

          window.speechSynthesis.speak(utterance);
        });
      } else {
        console.warn('Tu navegador no soporta síntesis de voz.');
      }
    },

    // Dividir texto largo en fragmentos más pequeños
    dividirTextoEnFragmentos(texto) {
      const longitudMaxima = 200;
      return texto.match(new RegExp(`.{1,${longitudMaxima}}`, 'g')) || [texto];
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
  color: #333;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>

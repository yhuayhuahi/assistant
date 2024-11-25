<template>
  <div>
    <h1>Speech to Text</h1>
    <button @click="startRecognition">Start Recognition</button>
    <button @click="stopRecognition">Stop Recognition</button>
    <p>Transcription: {{ transcription }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      recognition: null,
      transcription: '',
    };
  },
  mounted() {
    this.setupRecognition();
  },
  methods: {
    setupRecognition() {
      // Verifica que el navegador soporte la API de Web Speech
      if ('webkitSpeechRecognition' in window) {
        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = true; // Escucha continuamente
        this.recognition.interimResults = true; // Resultados intermedios mientras hablas
        this.recognition.lang = 'es-ES'; // Configura el idioma (puedes usar 'en-US' para inglés)
        
        // Cuando se obtiene un resultado
        this.recognition.onresult = (event) => {
          let transcript = '';
          for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
          }
          this.transcription = transcript;
        };

        // Maneja los errores
        this.recognition.onerror = (event) => {
          console.error('Error de reconocimiento de voz:', event.error);
        };
      } else {
        alert('Web Speech API no está soportada en este navegador.');
      }
    },
    startRecognition() {
      if (this.recognition) {
        this.recognition.start(); // Comienza la captura de voz
      }
    },
    stopRecognition() {
      if (this.recognition) {
        this.recognition.stop(); // Detiene la captura de voz
      }
    },
    async sendToBackend() {
      if (this.transcription.trim() !== '') {
        // Aquí construimos el JSON con el campo "mensaje"
        const message = {
          mensaje: this.transcription,
        };

        // Enviar el mensaje transcrito al backend
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/front/', message, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          console.log('Mensaje enviado:', response.data);
        } catch (error) {
          console.error('Error al enviar el mensaje:', error);
        }
      }
    },
  },
  watch: {
    // Enviar al backend cada vez que se actualiza la transcripción
    transcription(newText) {
      if (newText.trim() !== '') {
        this.sendToBackend();
      }
    },
  },
};
</script>

<style scoped>
button {
  padding: 10px 20px;
  margin: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

p {
  font-size: 18px;
}
</style>

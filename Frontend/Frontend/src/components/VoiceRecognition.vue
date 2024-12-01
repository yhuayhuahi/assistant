<template>
  <div>
    <h1>Speech to Text</h1>
    <button @click="toggleRecognition">
      {{ isRecognizing ? 'Detener' : 'Iniciar' }} Reconocimiento
    </button>
    <p>Transcripción: {{ transcription }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      recognition: null,
      transcription: '',
      isRecognizing: false, // Estado para saber si el micrófono está activo
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
        this.recognition.continuous = false; // No escucha continuamente
        this.recognition.interimResults = true; 
        this.recognition.lang = 'es-ES'; // Idioma

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

        // Cuando el reconocimiento se detiene o se completa
        this.recognition.onend = () => {
          this.isRecognizing = false; // El micrófono está apagado
        };
      } else {
        alert('Web Speech API no está soportada en este navegador.');
      }
    },
    toggleRecognition() {
      if (this.isRecognizing) {
        this.stopRecognition();
      } else {
        this.startRecognition();
      }
    },
    startRecognition() {
      if (this.recognition) {
        this.recognition.start(); // Inicia la captura de voz
        this.isRecognizing = true; // Cambia el estado para indicar que el micrófono está activo
      }
    },
    stopRecognition() {
      if (this.recognition) {
        this.recognition.stop(); // Detiene la captura de voz
        this.isRecognizing = false; // Cambia el estado para indicar que el micrófono está apagado
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

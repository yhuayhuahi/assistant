<template>
  <div id="app">
    <h1>Asistente Virtual</h1>
    <button @click="iniciarVoz">Hablar</button>
    
    <div v-if="mensaje">
      <h2>Texto del mensaje:</h2>
      <p>{{ mensaje }}</p>
    </div>

    <button v-if="mensaje" @click="enviarMensaje">Enviar</button>

    <div v-if="respuesta">
      <h2>Respuesta del Asistente:</h2>
      <p>{{ respuesta }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mensaje: "",
      respuesta: "",
      reconocimiento: null,  // Para manejar el reconocimiento de voz
    };
  },
  methods: {
    // Iniciar la grabación de voz
    iniciarVoz() {
      if (!("webkitSpeechRecognition" in window)) {
        alert("Tu navegador no soporta reconocimiento de voz.");
        return;
      }

      // Crear una nueva instancia del reconocimiento de voz
      this.reconocimiento = new webkitSpeechRecognition();
      this.reconocimiento.continuous = false;  // Solo reconocer una vez
      this.reconocimiento.lang = "es-ES";  // Configurar el idioma (en este caso, español)
      this.reconocimiento.interimResults = false;  // Solo resultados finales

      // Callback cuando se detecta el resultado
      this.reconocimiento.onresult = (event) => {
        const texto = event.results[0][0].transcript;
        this.mensaje = texto;  // Establecer el mensaje con lo que se reconoció
      };

      // Callback para errores
      this.reconocimiento.onerror = (event) => {
        alert("Hubo un error con el reconocimiento de voz: " + event.error);
      };

      // Iniciar el reconocimiento de voz
      this.reconocimiento.start();
    },

    // Enviar el mensaje al backend
    async enviarMensaje() {
      try {
        const response = await axios.post("http://localhost:8000/api/front/", {
          mensaje: this.mensaje,
        });

        // Manejar la respuesta del backend
        if (response.data.message) {
          this.respuesta = response.data.message;
        } else if (response.data.error) {
          this.respuesta = `Error: ${response.data.error}`;
        }
      } catch (error) {
        console.error(error);
        this.respuesta = "Hubo un error al procesar tu solicitud.";
      }
    },
  },
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 50px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

h1, h2 {
  font-size: 24px;
  font-weight: bold;
}

p {
  font-size: 18px;
  margin-top: 20px;
}
</style>

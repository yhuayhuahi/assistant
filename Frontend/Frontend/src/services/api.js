import axios from 'axios';

export default {
  data() {
    return {
      mensajeUsuario: '', // El mensaje que el usuario ingresa
      respuestaAsistente: '', // La respuesta del asistente
    };
  },
  methods: {
    enviarMensaje() {
      // Envía el mensaje del usuario al backend
      axios.post('http://localhost:8000/api/front/', {
        mensaje: this.mensajeUsuario
      })
      .then(response => {
        // Maneja la respuesta del backend
        this.respuestaAsistente = response.data.message;
      })
      .catch(error => {
        console.error('Hubo un error:', error);
      });
    }
  }
}

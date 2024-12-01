import { createRouter, createWebHistory } from 'vue-router';
import App from '../App.vue';
import AsistentePsicologico from '../components/AsistentePsicologico.vue';

const routes = [
  { path: '/', component: App }, // Ruta principal
  { path: '/asistente', component: AsistentePsicologico }  // Ruta para el asistente psicológico
];

const router = createRouter({
  history: createWebHistory(),  // Usar historial de navegación
  routes,
});

export default router;

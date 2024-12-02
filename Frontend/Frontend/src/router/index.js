import { createRouter, createWebHistory } from 'vue-router';
import MicControl from '../components/MicControl.vue';
import AsistentePsicologico from '../components/AsistentePsicologico.vue'; // Componente del asistente

const routes = [
  {
    path: '/',
    name: 'Inicio',
    component: MicControl
  },
  {
    path: '/asistente-psicologico',
    name: 'AsistentePsicologico',
    component: AsistentePsicologico
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

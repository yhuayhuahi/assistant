from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, TareaViewSet, usuario_tarea, lenguaje_natural, api_overview, chat_psycology

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tareas', TareaViewSet)

urlpatterns = [
    path('prueba/', api_overview, name='api-overview'),
    path('', include(router.urls)),
    path('usuarios-tareas/', usuario_tarea, name='usuarios_tareas'),
    path('front/', lenguaje_natural, name='coneccion_directa'),
    path('asistente-psicologico/', chat_psycology, name='asistente_psicologico')
]

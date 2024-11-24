from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, TareaViewSet, api_overview

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tareas', TareaViewSet)

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('', include(router.urls)),
]

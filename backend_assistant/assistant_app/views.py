#from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from .models import Usuario, Tarea
from .serializers import UsuarioSerializer, TareaSerializer

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TareaViewSet(ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

@api_view(['GET'])
def api_overview(request):
    return Response({"message": "Bienvenido a la API del asistente virtual"})

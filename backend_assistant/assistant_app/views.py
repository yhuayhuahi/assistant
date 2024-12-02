#from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
import json

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.test import APIClient

from rest_framework.viewsets import ModelViewSet
from .models import Usuario, Tarea
from .serializers import UsuarioSerializer, TareaSerializer

# Coneccion con cohere.ai
from scripts.general import API_KEY, COMANDOS
from scripts.virtual_assistant_app import run
from cohere import ClientV2

import re
from dateutil import parser

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TareaViewSet(ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

@api_view(['POST', 'GET', 'PUT'])
def usuario_tarea(request):
    if request.method == 'GET':
        """
        Maneja las solicitudes GET.
        Retorna una lista de todos los usuarios y sus tareas relacionadas.
        """
        usuarios = Usuario.objects.all()
        response_data = []
        
        for usuario in usuarios:
            tareas = Tarea.objects.filter(usuario=usuario)
            usuario_data = model_to_dict(usuario)
            usuario_data['audio'] = usuario.audio.url if usuario.audio else None
            
            response_data.append({
                'usuario': usuario_data,
                'tareas': [model_to_dict(tarea) for tarea in tareas]
            })
        
        return JsonResponse({'data': response_data}, safe=False, status=200)

    elif request.method == 'POST':
        """
        Maneja las solicitudes POST.
        Crea un usuario o una tarea basada en los datos recibidos.
        """
        try:
            body = json.loads(request.body)
            
            # Crear una nueva tarea
            if 'usuario' in body and 'nombre' in body and 'fecha_planificada' in body:
                usuario = Usuario.objects.get(id=body['usuario'])
                nueva_tarea = Tarea.objects.create(
                    usuario=usuario,
                    nombre=body['nombre'],
                    fecha_planificada=body['fecha_planificada']
                )
                return JsonResponse({'message': 'Tarea creada', 'tarea': model_to_dict(nueva_tarea)}, status=201)
            
            # Crear un nuevo usuario
            elif 'nombre' in body and 'usuario' not in body:
                audio = body.get('audio', None)
                email = body.get('email', None)

                nuevo_usuario = Usuario.objects.create(
                    nombre=body['nombre'],
                    audio=audio,
                    email=email
                )
                usuario_data = model_to_dict(nuevo_usuario)
                usuario_data['audio'] = nuevo_usuario.audio.url if nuevo_usuario.audio else None
                
                return JsonResponse({'message': 'Usuario creado', 'usuario': usuario_data}, status=201)
            
            else:
                return JsonResponse({'error': 'Datos incompletos o formato no válido'}, status=400)
        
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos no válidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'PUT':
        """
        Maneja las solicitudes PUT.
        Actualiza información de un usuario o una tarea.
        """
        try:
            body = json.loads(request.body)
            
            # Actualizar un usuario
            if 'usuario_id' in body:
                usuario = Usuario.objects.get(id=body['usuario_id'])
                if 'nombre' in body:
                    usuario.nombre = body['nombre']
                if 'email' in body:
                    usuario.email = body['email']
                if 'audio' in body:
                    usuario.audio = body['audio']
                usuario.save()
                usuario_data = model_to_dict(usuario)
                usuario_data['audio'] = usuario.audio.url if usuario.audio else None
                return JsonResponse({'message': 'Usuario actualizado', 'usuario': usuario_data}, status=200)
            
            # Actualizar una tarea
            elif 'tarea_id' in body:
                tarea = Tarea.objects.get(id=body['tarea_id'])
                if 'nombre' in body:
                    tarea.nombre = body['nombre']
                if 'fecha_planificada' in body:
                    tarea.fecha_planificada = body['fecha_planificada']
                if 'completada' in body:
                    tarea.completada = body['completada']
                tarea.save()
                return JsonResponse({'message': 'Tarea actualizada', 'tarea': model_to_dict(tarea)}, status=200)
            
            else:
                return JsonResponse({'error': 'Datos incompletos o formato no válido'}, status=400)
        
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuario o tarea no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos no válidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def lenguaje_natural(request):
    try:
        # Parsear el cuerpo de la solicitud
        body = json.loads(request.body)
        mensaje_usuario = body.get('mensaje')

        if not mensaje_usuario:
            return JsonResponse({'error': 'Mensaje no proporcionado'}, status=400)
        
        # Inicializar cliente de Cohere
        co = ClientV2(API_KEY)
        
        # Crear el mensaje de entrada para el modelo
        contexto = {
            "role": "user",
            "content": (
                "Eres un asistente virtual que puede realizar acciones de acuerdo a los comando que te mostrare, si algo coincide con algún comando no dudes, en caso de que no se pueda, hay respuestas en otra parte del código\n"
                f"Tengo una lista de comandos disponibles:\n{', '.join(COMANDOS)}.\n"
                f"El usuario dice: '{mensaje_usuario}'.\n"
                "Identifica lo que el usuario quiere y devuelve lo siguiente:\n"
                "- Si coincide con un comando, responde con {'accion': '<comando>', 'contenido': '<mensaje>'}.\n"
                "- Si lo que quiere no coincide con un comando, indica {'accion': 'self', 'contenido': '<mensaje>'}.\n"
                "- Si el usuario quiere guardar una tarea, responde con {'accion': 'guardar tarea', 'contenido': '<nombre de la tarea>', 'fecha': 'AAAA-MM-DD'}.\n"
            )
        }

        # Llamar al modelo Cohere con el mensaje
        response = co.chat(
            model="command-r-plus",
            messages=[contexto]
        )
        
        # Extraer y limpiar la respuesta del modelo
        respuesta = response.message.content[0].text.strip()
        print(respuesta)

        # Usar una expresión regular para extraer los atributos 'accion' y 'contenido' (y 'fecha' si es necesario)
        pattern = r"'\s*accion'\s*:\s*'([^']+)'\s*,\s*'contenido'\s*:\s*'([^']+)'(?:\s*,\s*'fecha'\s*:\s*'([^']+)')?"

        match = re.search(pattern, respuesta)

        if not match:
            return JsonResponse({'error': 'No se pudo extraer la información necesaria de la respuesta'}, status=500)

        # Obtener los valores de los grupos
        accion = match.group(1)
        contenido = match.group(2)
        fecha = match.group(3) if match.group(3) else None  # Si 'fecha' no está presente, lo dejamos como None

        # Lógica para manejar la respuesta
        client = APIClient()
        if accion == 'guardar tarea' and fecha:
            # Crear una tarea mediante la API
            response = client.post('/api/tareas/', {'usuario': 1, 'nombre': contenido, 'fecha_planificada': fecha})
            response_data = response.json()  # Convertir la respuesta a JSON

            try:
                # Obtener los datos de la tarea creada
                nombre = response_data.get('nombre', 'Sin nombre')
                fecha_planificada = response_data.get('fecha_planificada', 'Sin fecha')

                # Crear el contexto para Cohere
                contexto = {
                    "role": "user",
                    "content": (
                        "Eres un asistente virtual. Quiero que leas lo siguiente y lo pongas en una forma que pueda leer un asistente de voz\n"
                        f"La tarea es {nombre} - {fecha_planificada}.\n"
                    )
                }

                # Llamar al modelo Cohere con el mensaje
                response2 = co.chat(
                    model="command-r-plus",
                    messages=[contexto]
                )

                # Extraer contenido de la respuesta de Cohere
                contenido_generado = "\n".join([item.text for item in response2.message.content])  # Ajusta según la estructura de `response2`

                # Responder al cliente
                return JsonResponse({'message': contenido_generado, 'accion': accion}, status=200)
            except AttributeError as e:
                return JsonResponse({'error': f"Atributo no encontrado: {str(e)}"}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        elif accion == 'mostrar tareas':
            # Obtener tareas de la API
            response = client.get('/api/tareas/')
            response_data = response.json()  # Convertir a JSON

            # Formatear tareas
            formato = "\n".join([
                f"{tarea.get('nombre', 'Sin nombre')} - {tarea.get('fecha_planificada', 'Sin fecha')}"
                for tarea in response_data
            ])

            # Crear el contexto para el modelo
            contexto = {
                "role": "user",
                "content": (
                    "Eres un asistente virtual. Quiero que leas lo siguiente y lo pongas en una forma que pueda leer un asistente de voz:\n"
                    f"Tareas pendientes:\n{formato}\n"
                )
            }

            # Llamar al modelo Cohere con el mensaje
            response2 = co.chat(
                model="command-r-plus",
                messages=[contexto]
            )

            # Acceder correctamente al texto generado por Cohere
            try:
                mensaje_generado = response2.message.content[0].text  # Usa el atributo correcto según la documentación de Cohere
                return JsonResponse({'message': mensaje_generado, 'accion': accion}, status=200)
            except AttributeError as e:
                return JsonResponse({'error': f"Atributo no encontrado: {str(e)}"}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        elif accion == 'eliminar tarea':
            # Eliminar una tarea
            # Obtener tareas de la API
            response = client.get('/api/tareas/')
            response_data = response.json()  # Convertir a JSON

            # Formatear tareas
            formato = "\n".join([
                f"{tarea.get('id')} - {tarea.get('nombre', 'Sin nombre')} - {tarea.get('fecha_planificada', 'Sin fecha')}"
                for tarea in response_data
            ])

            # Crear el contexto para el modelo
            contexto = {
                "role": "user",
                "content": (
                    f"Quiero que reconozcas si {contenido}, se refiere a una de estas tareas:\n"
                    f"Tareas pendientes:\n{formato}\n"
                    "En caso de que sea una de ellas, retorna su id para eliminarla.\n"
                )
            }

            # Llamar al modelo Cohere con el mensaje
            response2 = co.chat(
                model="command-r-plus",
                messages=[contexto]
            )
            
            id = int(response2.message.content[0].text)
            
            response = client.delete(f'/api/tareas/{id}/')
            return JsonResponse({'message': 'Tarea eliminada con exito', 'accion': accion}, status=200)
        
        else:
            # Si no es una tarea, simplemente devolvemos la acción y el contenido
            respuesta = run(accion + ' ' + contenido)
            return JsonResponse({'message': respuesta, 'accion': accion}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error en el formato JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def assistant_psycology(request):
    # Parsear el cuerpo de la solicitud
    body = json.loads(request.body)
    mensaje_usuario = body.get('mensaje')

    if not mensaje_usuario:
        return JsonResponse({'error': 'Mensaje no proporcionado'}, status=400)
    
    # Inicializar cliente de Cohere
    co = ClientV2(API_KEY)
    
    contexto = 'Eres un asistente virtual de ayuda psicologica y/o emocional, responde a las siguientes preguntas de acuerdo a tu conocimiento y experiencia\n'
    
    # Crear el mensaje de entrada para el modelo
    response = co.chat(
        model="command-r-plus",
        messages=[
            {
                "role": "user",
                "content": contexto
            },
            {
                "role": "assistant",
                "content": "Entendido!"
            },
            {
                "role": "user",
                "content": mensaje_usuario
            }
        ]
    )
    
    respuesta = response.message.content[0].text
    return JsonResponse({'message': respuesta}, status=200)


@api_view(['GET'])
def api_overview(request):
    return Response({"message": "Bienvenido a la API del asistente virtual"})


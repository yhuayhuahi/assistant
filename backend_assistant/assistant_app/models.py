from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_audio = models.FileField(upload_to='audios_usuarios/', help_text="Archivo de audio identificador del usuario")
    nombre = models.CharField(max_length=100, help_text="Nombre del usuario")
    email = models.EmailField(blank=True, null=True, help_text="Correo electrónico opcional")

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas', help_text="Usuario al que pertenece esta tarea")
    nombre = models.CharField(max_length=255, help_text="Nombre de la tarea")
    fecha_planificada = models.DateField(help_text="Fecha planificada para completar la tarea")
    completada = models.BooleanField(default=False, help_text="Indica si la tarea ha sido completada")

    def __str__(self):
        return f"{self.nombre} - {self.usuario.nombre}"

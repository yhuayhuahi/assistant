# -*- coding: utf-8 -*-

from .reproductor import play_song_in_browser
from .ubicacion_temporal import tiempo
from .apps import ejecutar_comando

import pywhatkit
import wikipedia
import chistesESP as chistes

"""LENGUAJE DE WIKIPEDIA"""
wikipedia.set_lang('es')

# Metodo que ejecuta al asistente
def run(recognizer = 'busca en google animales'):

    # REPRODUCE UN VIDEO EN YOUTUBE
    if 'reproduce' in recognizer:
        music = recognizer.replace('reproduce', '')
        return play_song_in_browser(music)

    # BUSCA EN WIKIPEDIA
    elif 'busca en wikipedia' in recognizer:
        consulta = recognizer.replace('busca en wikipedia', '')
        resultado = wikipedia.summary(consulta, sentences=3)
        return (resultado)
    
    # INDICA LA UBICACION TEMPORAL
    elif tiempo(recognizer)[0]:
        return (tiempo(recognizer)[1])

    # BUSCA EN GOOGLE
    elif 'busca en google' in recognizer:
        consulta = recognizer.replace('busca en google', '')
        pywhatkit.search(consulta)
        return ('Buscando en google' + consulta)

    # CHISTES
    elif 'chiste' in recognizer:
        chiste = chistes.get_random_chiste()
        return (chiste)
    
    # ABRIR APPS
    elif 'abre la aplicacion' in recognizer:
        app = recognizer.replace('abre la app', 'abre')
        ejecutar_comando(recognizer)
        return ('Abriendo ' + app)

    else:
        return('Disculpa, no puedo realizar esa acción')
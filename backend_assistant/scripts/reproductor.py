from youtubesearchpython import VideosSearch

import webbrowser
import pygetwindow as gw
import time

PATH = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

# Función para buscar y obtener el enlace del primer resultado
def get_first_youtube_result(query):
    videos_search = VideosSearch(query, limit=1)
    results = videos_search.result()
    first_result = results['result'][0]['link']  # Enlace del primer resultado
    return first_result

# Funcion para reproducir en brave
def play_in_brave(music_url):
    brave_path = PATH

    # Registrar Brave como navegador personalizado
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
    
    # Abre el navegador Brave con la búsqueda de YouTube
    webbrowser.get('brave').open(music_url)

# Funcion para minimizar la ventana de windows
def minimize_window():
    # Busca todas las ventanas activas
    windows = gw.getAllTitles()
    for win in windows:
        if "brave" in win.lower():  # Busca por nombre de la ventana (Brave)
            window = gw.getWindowsWithTitle(win)[0]
            window.minimize()  # Minimiza la ventana
            break

def play_song_in_browser(music):
    #pywhatkit.playonyt(music)
    music_url = get_first_youtube_result(music)
    play_in_brave(music_url)

    # Espera unos segundos para asegurarte de que el navegador abre
    time.sleep(1/2)

    # Minimiza la ventana del navegador
    minimize_window()
    return (f'Reproduciendo {music}')
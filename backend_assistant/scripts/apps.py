import os

from .general import API_KEY
from cohere import ClientV2

# Diccionario con el nombre de la aplicación y la ruta de su ejecutable
aplicaciones_dict = {
    "adobe audition": r"C:\Program Files\Adobe\Adobe Audition CC 2018\Adobe Audition CC.exe",
    "internet explorer": r"C:\Program Files\Internet Explorer\iexplore.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "one note": r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
    "access": r"C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "pdfelement": r"C:\Program Files\Wondershare\PDFelement10\PDFelement.exe",
    "brave": r"C:\Users\YOURDYY\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
    "notepad": r"C:\Windows\notepad.exe",
    "terabox": r"C:\Users\YOURDYY\AppData\Roaming\TeraBox\TeraBox.exe",
    "calculadora": r"C:\Windows\System32\calc.exe",
}

# Función para obtener la ruta del ejecutable según el nombre de la aplicación
def obtener_ejecutable(nombre_aplicacion):
    return aplicaciones_dict.get(nombre_aplicacion.lower())  # Retorna la ruta si existe, si no, None

# Función para abrir la aplicación usando la ruta de su ejecutable
def abrir_aplicacion(nombre_aplicacion):
    ejecutable = obtener_ejecutable(nombre_aplicacion)
    
    if ejecutable:
        try:
            # Agregar comillas a la ruta si contiene espacios
            os.system(f'"{ejecutable}"')
            print(f"{nombre_aplicacion} se está abriendo...")
        except Exception as e:
            print(f"Ocurrió un error al intentar abrir {nombre_aplicacion}: {e}")
    else:
        print(f"No se encontró el ejecutable para {nombre_aplicacion}")

def interpretar_comando(comando_usuario, aplicaciones):
    co = ClientV2(API_KEY)
    
    mensaje = (
        f"Tengo una lista de aplicaciones instaladas:\n{', '.join(aplicaciones)}.\n"
        f"El usuario dice: '{comando_usuario}'.\n"
        "Devuélveme el nombre exacto de la aplicación que coincide con lo que el usuario pide, "
        "o indica 'ninguna' si no hay coincidencias."
    )
    
    response = co.chat(
        model="command-r-plus", 
        messages=[{
            "role": "user", 
            "content": mensaje
        }]
    )
    print(response.message.content[0].text)
    return response.message.content[0].text

def ejecutar_comando(comando_usuario):
    # Aquí se asume que ya tienes un diccionario de aplicaciones
    aplicaciones = aplicaciones_dict.keys()
    
    # Interpretamos el comando del usuario
    nombre_aplicacion = interpretar_comando(comando_usuario, aplicaciones)
    
    # Abrimos la aplicación si se encontró
    if nombre_aplicacion != 'ninguna':
        abrir_aplicacion(nombre_aplicacion)
        return (f"Abriendo {nombre_aplicacion}...")
    else:
        return (f"No se encontró una aplicación que coincida con '{comando_usuario}'")

# Ejemplo de uso
#print(ejecutar_comando('abre internet explorer porfabor'))
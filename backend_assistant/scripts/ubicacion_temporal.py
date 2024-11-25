import datetime as time

# Traduccion de los meses
spanish_month = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}

def tiempo( comando ):
    confirmacion = False
    respuesta = ''
    
    palabras_clave = ['hora', 'fecha', 'dia', 'mes', 'año']
    for palabra in palabras_clave:
        if palabra in comando:
            confirmacion = True
    
    if confirmacion:
        if palabras_clave[0] in comando:
            hora = time.datetime.now().strftime('%I:y%M %p')
            respuesta = 'Son las '+hora
        elif palabras_clave[1] in comando:
            fecha = time.datetime.now().strftime('%d-%h-%Y')
            respuesta = 'La fecha es: ' + str(fecha)
        elif palabras_clave[2] in comando:
            dia = time.datetime.now().strftime('%d')
            respuesta = 'Hoy es el día ' + str(dia)
        elif palabras_clave[3] in comando:
            mes = time.datetime.now().strftime('%B')
            mes_translate = spanish_month[mes]
            respuesta = 'Estamos en el mes de ' + str(mes_translate)
        else:
            year = time.datetime.now().strftime('%Y')
            respuesta = 'Estamos en el ' + str(year)
    
    return [confirmacion, respuesta]
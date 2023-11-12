import csv
import os
import datetime

# Variables globales que usaremos en este módulo
prestamos = []
id_prestamos = 1  # Variable para asignar IDs únicos a los prestamos
ruta_archivo_prestamos = 'modelos\\prestamos.csv'

# estructura: id,socio_dni,libro_id,fecha_retiro,fecha_devolucion

def inicializar_prestamos():
    global id_prestamos
    if os.path.exists(ruta_archivo_prestamos):
        importar_datos_desde_csv()

def crear_prestamo(socio_id,libro_id,fecha_retiro,fecha_devolucion):
    global id_prestamos
    # Agrega el prestamo a la lista con un ID único
    prestamos.append({
        "id": id_prestamos,
        "socio_id": socio_id,
        "libro_id": libro_id,
        "fecha_retiro": fecha_retiro,
        "fecha_devolucion": fecha_devolucion
    })
    id_prestamos += 1
    exportar_a_csv()
    # Devuelve el prestamo recién creado
    return prestamos[-1]

def obtener_prestamo_por_id(id_prestamos):
    # Recorre la lista de prestamos
    for prestamo in prestamos:
        # Si el ID de prestamo coincide, devuelve el prestamo
        if prestamo["id"] == id_prestamos:
            return prestamo
    # Devuelve None si no se encuentra el prestamo
    return None

def obtener_prestamos():
    # Devuelve la lista de prestamos
    return prestamos

def obtener_prestamos_sin_devolver():
    # Devuelve la lista de prestamos que aún no se han devuelto
    prestamos_sin_devolver = []
    for prestamo in prestamos:
        # puede ser que el prestamo no tenga cargada la fecha de devolución, o que se haya pactado una devolucion futura, esto no estaba especificado en la consigna
        if prestamo["fecha_devolucion"] == "" or datetime.datetime.strptime(prestamo["fecha_devolucion"]) > datetime.datetime.now():
            prestamos_sin_devolver.append(prestamo)
    return prestamos_sin_devolver

def editar_prestamo_por_id(id_prestamos,socio_id,libro_id,fecha_retiro,fecha_devolucion):
    # Recorre la lista de prestamos
    for prestamo in prestamos:
        
        if prestamo["id"] == id_prestamos:
            prestamo["socio_id"] = socio_id
            prestamo["libro_id"] = libro_id
            prestamo["fecha_retiro"] = fecha_retiro
            prestamo["fecha_devolucion"] = fecha_devolucion
            exportar_a_csv()
            return prestamo
    # Devuelve None si no se encuentra el prestamo
    return None

def eliminar_prestamo_por_id(id_usuario):
    global prestamos
    # Crea una nueva lista sin el prestamo a eliminar
    prestamo_a_eliminar = [prestamo for prestamo in prestamos if prestamo["id"] == id_usuario]
    if len(prestamo_a_eliminar) > 0:
        # puede ser que el prestamo no tenga cargada la fecha de devolución, o que se haya pactado una devolucion futura,
        # en ese caso no lo elimino porque todavia no se devolvio el libro
        if prestamo_a_eliminar[0]["fecha_devolucion"] == "" or datetime.datetime.strptime(prestamo_a_eliminar[0]["fecha_devolucion"]) > datetime.datetime.now():
            return None
        else:
            prestamos.remove(prestamo_a_eliminar[0])
            exportar_a_csv()
            return prestamo_a_eliminar[0]
    else:
        return None

def exportar_a_csv():
    """
    Exporta los datos de prestamos a un archivo CSV.
    """
    with open(ruta_archivo_prestamos, 'w', newline='', encoding='utf8') as csvfile:
        campo_nombres = ['id','socio_id','libro_id','fecha_retiro','fecha_devolucion']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for prestamo in prestamos:
            writer.writerow(prestamo)

def importar_datos_desde_csv():
    """
    Importa los datos de prestamos desde un archivo CSV.
    """
    global prestamos
    global id_prestamos
    prestamos = []  # Limpiamos la lista de prestamos antes de importar desde el archivo CSV
    with open(ruta_archivo_prestamos, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            row['socio_id'] = int(row['socio_id'])
            row['libro_id'] = int(row['libro_id'])
            prestamos.append(row) 
    if len(prestamos)>0:
        id_prestamos= prestamos[-1]["id"]+1
    else:
        id_prestamos = 1
import csv
import os

# Variables globales que usaremos en este módulo
socios = []
id_socio = 1  # Variable para asignar IDs únicos a los usuarios
ruta_archivo_socios = 'modelos\\socios.csv'

# estructura: id,dni,nombre,apellido,telefono,email

def inicializar_socios():
    global id_socio
    if os.path.exists(ruta_archivo_socios):
        importar_datos_desde_csv()

def crear_usuario(dni,nombre,apellido,telefono,email):
    global id_socio
    # Agrega el usuario a la lista con un ID único
    socios.append({
        "id": id_socio,
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email
    })
    id_socio += 1
    exportar_a_csv()
    # Devuelve el usuario recién creado
    return socios[-1]

def obtener_socio_por_id(id_socio):
    # Recorre la lista de socios
    for socio in socios:
        # Si el ID de socio coincide, devuelve el usuario
        if socio["id"] == id_socio:
            return socio
    # Devuelve None si no se encuentra el usuario
    return None

def obtener_socios():
    # Devuelve la lista de socios
    return socios

def editar_socio_por_id(id_socio,dni,nombre,apellido,telefono,email):
    # Recorre la lista de socios
    for socio in socios:
        # Si el ID de socio coincide, actualiza el nombre de usuario y la contraseña
        if socio["id"] == id_socio:
            socio["dni"] = dni
            socio["nombre"] = nombre
            socio["apellido"] = apellido
            socio["telefono"] = telefono
            socio["email"] = email
            exportar_a_csv()
            return socio
    # Devuelve None si no se encuentra el usuario
    return None

def eliminar_usuario_por_id(id_usuario):
    global socios
    # Crea una nueva lista sin el usuario a eliminar
    socios = [usuario for usuario in socios if usuario["id"] != id_usuario]
    exportar_a_csv()

def exportar_a_csv():
    """
    Exporta los datos de socios a un archivo CSV.
    """
    with open(ruta_archivo_socios, 'w', newline='') as csvfile:
        campo_nombres = ['id','dni','nombre','apellido','telefono','email']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for socio in socios:
            writer.writerow(socio)

def importar_datos_desde_csv():
    """
    Importa los datos de socios desde un archivo CSV.
    """
    global socios
    global id_socio
    socios = []  # Limpiamos la lista de usuarios antes de importar desde el archivo CSV
    with open(ruta_archivo_socios, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            row['dni'] = int(row['dni'])
            socios.append(row) 
    if len(socios)>0:
        id_socio= socios[-1]["id"]+1
    else:
        id_socio = 1
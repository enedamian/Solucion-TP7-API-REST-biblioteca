import os, csv

# Variables globales que usaremos en este módulo
libros = []
id_libro = 1  # Variable para asignar IDs únicos a los libros
ruta_archivo_libros = 'modelos\\libros.csv'

# estructura: id,titulo,autor,anio_publicacion

def inicializar_libros():
    """
    Inicializa la variable global id_libro y verifica si existe el archivo de datos de libros.
    Si existe, importa los datos desde el archivo CSV correspondiente.
    """
    global id_libro
    if os.path.exists(ruta_archivo_libros):
        importar_datos_desde_csv()

def crear_libro(titulo,autor,anio_publicacion):
    """
    Crea un nuevo libro con los datos proporcionados y lo agrega a la lista de libros.

    Args:
        titulo (str): El título del libro.
        autor (str): El autor del libro.
        anio_publicacion (int): El año de publicación del libro.

    Returns:
        dict: Un diccionario que representa el libro recién creado.
    """
    global id_libro
    # Agrega el libro a la lista con un ID único
    libros.append({
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "anio_publicacion": anio_publicacion
    })
    id_libro += 1
    exportar_a_csv()
    # Devuelve el libro recién creado
    return libros[-1]

def obtener_libro_por_id(id):
    """
    Devuelve el libro con el ID especificado.

    Parámetros:
    id (int): El ID del libro a buscar.

    Retorna:
    dict: El diccionario que representa al libro encontrado, o None si no se encuentra.
    """
    # Recorre la lista de libros
    for libro in libros:
        # Si el ID del libro coincide, devuelve el libro
        if libro["id"] == id:
            return libro
    # Devuelve None si no se encuentra el libro
    return None

def obtener_libros():
    """
    Devuelve la lista de libros.

    Returns:
    list: Una lista de diccionarios que representan los libros.
    """
    return libros

def editar_libro_por_id(id,titulo,autor,anio_publicacion):
    """
    Edita un libro en la lista de libros por su ID.

    Parámetros:
    id (int): El ID del libro a editar.
    titulo (str): El nuevo título del libro.
    autor (str): El nuevo autor del libro.
    anio_publicacion (int): El nuevo año de publicación del libro.

    Retorna:
    dict: El diccionario del libro editado.
    None: Si no se encuentra el libro con el ID especificado.
    """
    # Recorre la lista de libros
    for libro in libros:
        if libro["id"] == id:
            libro["titulo"] = titulo
            libro["autor"] = autor
            libro["anio_publicacion"] = anio_publicacion
            exportar_a_csv()
            return libro
    # Devuelve None si no se encuentra el libro
    return None

def eliminar_libro_por_id(id):
    """
    Elimina un libro de la lista de libros por su ID.

    Args:
        id (int): El ID del libro a eliminar.

    Returns:
        None
    """
    global libros
    # Crea una nueva lista sin el libro a eliminar
    libros = [libro for libro in libros if libro["id"] != id]
    exportar_a_csv()

def exportar_a_csv():
    """
    Exporta los datos de los libros a un archivo CSV.
    """
    with open(ruta_archivo_libros, 'w', newline='', encoding='utf8') as csvfile:
        campo_nombres = ['id','titulo','autor','anio_publicacion']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for libro in libros:
            writer.writerow(libro)

def importar_datos_desde_csv():
    """
    Importa los datos de los libros desde un archivo CSV.
    """
    global libros
    global id_libro
    libros = []  # Limpiamos la lista de libros antes de importar desde el archivo CSV
    with open(ruta_archivo_libros, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            row['anio_publicacion'] = int(row['anio_publicacion'])
            libros.append(row) 
    if len(libros)>0:
        id_libro= libros[-1]["id"]+1
    else:
        id_libro = 1
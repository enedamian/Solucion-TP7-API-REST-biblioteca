from flask import Blueprint, jsonify, request
from modelos.libros import obtener_libros, obtener_libro_por_id, crear_libro, editar_libro_por_id, eliminar_libro_por_id

# la consigna pide rutas para:
# * Obtener la lista de todos los libros (`GET`).
# * Obtener detalles de un libro por su ID (`GET`).
# * Agregar un nuevo libro (`POST`). Debe recibir los datos en formato JSON.
# * Actualizar la información de un libro por su ID (`PUT`). Debe recibir los datos en formato JSON.

# Crear un blueprint
libros_bp = Blueprint('libros_bp', __name__)

@libros_bp.route('/libros', methods=['GET'])
def buscar_libros():
    libro = obtener_libros()
    if len(libro) > 0:
        return jsonify(libro), 200
    else:
        return jsonify({'error': 'No hay libros cargados'}), 404

@libros_bp.route('/libros/<int:id>', methods=['GET'])
def buscar_libro_id(id):
    libro = obtener_libro_por_id(id)
    if libro:
        return jsonify(libro), 200
    else:
        return jsonify({'error': 'Libro no encontrado'}), 404
    
@libros_bp.route('/libros', methods=['POST'])
def nuevo_libro():
    if request.is_json:
        if 'titulo' and 'autor' and 'anio_publicacion' in request.json:
            nuevo = request.get_json()
            libro = crear_libro(nuevo['titulo'], nuevo['autor'], nuevo['anio_publicacion'])
            return jsonify(libro), 201
        else:
            return jsonify({'error': 'Faltan datos para crear el libro'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400
    
@libros_bp.route('/libros/<int:id>', methods=['PUT'])
def editar_libro_id(id):
    if request.is_json:
        if 'titulo' and 'autor' and 'anio_publicacion' in request.json:
            libro = editar_libro_por_id(id, request.json['titulo'], request.json['autor'], request.json['anio_publicacion'])
            if libro:
                return jsonify(libro), 200
            else:
                return jsonify({'error': 'Libro no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos para editar el libro'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400
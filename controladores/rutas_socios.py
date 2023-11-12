from flask import Blueprint, jsonify, request
from modelos.socios import obtener_socios, obtener_socio_por_id, crear_socio, editar_socio_por_id, eliminar_socio_por_id

# la consigna pide rutas para:
# * Obtener la lista de todos los socios (`GET`).
# * Obtener detalles de un socio por su ID (`GET`).
# * Agregar un nuevo socio (`POST`). Debe recibir los datos en formato JSON.
# * Actualizar la información de un socio por su ID (`PUT`). Debe recibir los datos en formato JSON.
# * Eliminar un socio por su ID (`DELETE`). Realizar validaciones antes de eliminar el socio: no debe tener pendiente una devolución.

# Crear un blueprint
socios_bp = Blueprint('socios_bp', __name__)

@socios_bp.route('/socios', methods=['GET'])
def buscar_socios():
    socio = obtener_socios()
    if len(socio) > 0:
        return jsonify(socio), 200
    else:
        return jsonify({'error': 'No hay socios cargados'}), 404
    
@socios_bp.route('/socios/<int:id>', methods=['GET'])
def buscar_socio_id(id):
    socio = obtener_socio_por_id(id)
    if socio:
        return jsonify(socio), 200
    else:
        return jsonify({'error': 'Socio no encontrado'}), 404

@socios_bp.route('/socios', methods=['POST'])
def nuevo_socio():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo:
            socio_creado = crear_socio(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['email'])
            return jsonify(socio_creado), 201
        else:
            return jsonify({'error': 'Faltan datos para crear el socio'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

@socios_bp.route('/socios/<int:id>', methods=['PUT'])
def editar_socio_id(id):
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo:
            socio = editar_socio_por_id(id, nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['email'])
            if socio:
                return jsonify(socio), 200
            else:
                return jsonify({'error': 'Socio no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos para editar el socio'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

@socios_bp.route('/socios/<int:id>', methods=['DELETE'])
def eliminar_socio_id(id):
    socio = eliminar_socio_por_id(id)
    if socio:
        return jsonify(socio), 200
    else:
        return jsonify({'error': 'Socio no encontrado'}), 404
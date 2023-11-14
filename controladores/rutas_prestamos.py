from flask import Blueprint, jsonify, request
from modelos.prestamos import obtener_prestamos, obtener_prestamo_por_id, obtener_prestamos_sin_devolver, crear_prestamo, editar_prestamo_por_id, eliminar_prestamo_por_id, libro_prestado
from modelos.libros import existe_libro
from modelos.socios import existe_socio

# la consigna pide rutas para:
# * Obtener la lista de todos los libros prestados que aún no se han devuelto (`GET`).
# * Obtener detalles de un prestamo de libro por su ID (`GET`).
# * Generar un nuevo prestamo (`POST`). Debe recibir los datos en formato JSON.
# * Registrar la devolución de un prestamo por su ID (`PUT`). Debe recibir los datos en formato JSON.

# Crear un blueprint
prestamos_bp = Blueprint('prestamos_bp', __name__)

@prestamos_bp.route('/prestamos', methods=['GET'])
def buscar_prestamos():
    prestamo = obtener_prestamos()
    if len(prestamo) > 0:
        return jsonify(prestamo), 200
    else:
        return jsonify({'error': 'No hay prestamos cargados'}), 404
    
@prestamos_bp.route('/prestamos/<int:id>', methods=['GET'])
def buscar_prestamo_id(id):
    prestamo = obtener_prestamo_por_id(id)
    if prestamo:
        return jsonify(prestamo), 200
    else:
        return jsonify({'error': 'Prestamo no encontrado'}), 404

@prestamos_bp.route('/prestamos/pendientes', methods=['GET'])
def buscar_prestamos_sin_devolver():
    prestamo = obtener_prestamos_sin_devolver()
    if len(prestamo) > 0:
        return jsonify(prestamo), 200
    else:
        return jsonify({'error': 'No hay prestamos sin devolver'}), 404
    
@prestamos_bp.route('/prestamos', methods=['POST'])
def nuevo_prestamo():
    """
    Crea un nuevo préstamo a partir de los datos recibidos en formato JSON.
    Debe recibir todos los datos del préstamo, la fecha_devolucion debe estar en formato YYYY-MM-DD o en su defecto vacía.
    """
    if request.is_json:
        nuevo = request.get_json()
        if 'socio_id' in nuevo and 'libro_id' in nuevo and 'fecha_retiro' in nuevo and 'fecha_devolucion' in nuevo:
            if existe_libro(nuevo['libro_id']) :
                if existe_socio(nuevo['socio_id']):
                    prestamo_creado = crear_prestamo(nuevo['socio_id'], nuevo['libro_id'], nuevo['fecha_retiro'], nuevo['fecha_devolucion'])
                    return jsonify(prestamo_creado), 201
                else:
                    return jsonify({'error': 'Socio no encontrado'}), 404
            else:
                return jsonify({'error': 'Libro no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos para crear el prestamo'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

@prestamos_bp.route('/prestamos/<int:id>', methods=['PUT'])
def editar_prestamo_id(id):
    """
    Edita un préstamo a partir de los datos recibidos en formato JSON.
    Debe recibir todos los datos del préstamo, la fecha_devolucion debe estar en formato YYYY-MM-DD o en su defecto vacía.
    Esta ruta sirve para modificar un prestamo existente, y también sirve para registrar la devolución de un prestamo
    (incluyendo la fecha_devolucion con un valor distinto de vacío).
    """
    if request.is_json:
        nuevo = request.get_json()
        if 'socio_id' in nuevo and 'libro_id' in nuevo and 'fecha_retiro' in nuevo and 'fecha_devolucion' in nuevo:
            if existe_libro(nuevo['libro_id']) :
                if existe_socio(nuevo['socio_id']):
                    if not libro_prestado(nuevo['libro_id']):
                        prestamo = editar_prestamo_por_id(id, nuevo['socio_id'], nuevo['libro_id'], nuevo['fecha_retiro'], nuevo['fecha_devolucion'])
                        if prestamo:
                            return jsonify(prestamo), 200
                        else:
                            return jsonify({'error': 'Prestamo no encontrado'}), 404
                    else:
                        return jsonify({'error': 'El libro ya está prestado'}), 400
                else:
                    return jsonify({'error': 'Socio no encontrado'}), 404
            else:
                return jsonify({'error': 'Libro no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos para editar el prestamo'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400

@prestamos_bp.route('/prestamos/<int:id>', methods=['DELETE'])
def eliminar_prestamo_id(id):
    prestamo = eliminar_prestamo_por_id(id)
    if prestamo:
        return jsonify(prestamo), 200
    else:
        return jsonify({'error': 'Prestamo no encontrado'}), 404
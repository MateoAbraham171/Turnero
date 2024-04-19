from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_pacientes, obtener_paciente_por_id, crear_paciente, editar_paciente_por_id, eliminar_paciente_por_id

# Crear un blueprint
pacientes_bp = Blueprint('pacientes_bp', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def buscar_pacientes():
    paciente = obtener_pacientes()
    if len(paciente) > 0:
        return jsonify(paciente), 200
    else:
        return jsonify({'error': 'No hay pacientes cargados'}), 404

@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def buscar_paciente_id(id):
    paciente = obtener_paciente_por_id(id)
    if paciente:
        return jsonify(paciente), 200
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
@pacientes_bp.route('/pacientes', methods=['POST'])
def nuevo_paciente():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:         
            paciente_creado = crear_paciente(
                nuevo['dni'], nuevo['nombre'], nuevo['apellido'],
                nuevo['telefono'], nuevo['email'],
                nuevo['direccion_calle'], nuevo['direccion_numero']
            )
            return jsonify(paciente_creado), 201
        else:
            return jsonify({'error': 'Faltan datos para crear el paciente'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def editar_paciente_id(id):
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:
            paciente = editar_paciente_por_id(
                id, nuevo['dni'], nuevo['nombre'], nuevo['apellido'],
                nuevo['telefono'], nuevo['email'],
                nuevo['direccion_calle'], nuevo['direccion_numero']
            )
            if paciente:
                return jsonify(paciente), 200
            else:
                return jsonify({'error': 'Paciente no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan datos para editar el paciente'}), 400
    else:
        return jsonify({'error': 'No se recibió el formato JSON'}), 400
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente_id(id):
    paciente =eliminar_paciente_por_id(id)
    if paciente:
        return jsonify({'mensaje': 'Paciente eliminado exitosamente'}),200
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404





 
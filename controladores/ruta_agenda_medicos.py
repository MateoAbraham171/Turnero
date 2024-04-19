from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import obtener_agenda_ordenada, agregar_dia_horario, modifcar_dia_de_atencion, eliminar_dia_horario

#Crear blueprint
agenda_bp = Blueprint('agenda_bp', __name__)

@agenda_bp.route('/agenda_medicos', methods=['GET'])
def obtener_agenda_medicos():
    agenda = obtener_agenda_ordenada()
    if len(agenda) > 0:
        return jsonify(agenda), 200
    else:
        return jsonify({'error': 'No hay agenda de médicos'}), 404
    
@agenda_bp.route('/agenda_medicos', methods=['POST'])
def agregar_dia_y_horario(id_medico):
    if request.is_json:
        nuevo_dia = request.get_json()
        if 'dia_numero' in nuevo_dia and 'hora_inicio' in nuevo_dia and 'hora_fin' in nuevo_dia and 'id_medico' in nuevo_dia:
            agenda_formateada = agregar_dia_horario(nuevo_dia['dia_numero'], nuevo_dia['hora_inicio'], nuevo_dia['hora_fin'], id_medico)
            return agenda_formateada, 201
        else:
            return jsonify({'error': 'Datos incorrectos'}), 400
    else:
        return jsonify({'error': 'No se recibió información en formato JSON'}), 400
    
@agenda_bp.route('/agenda_medicos/<id_medico>', methods=['PUT'])
def modificar_agenda(id_medico):
    if request.is_json:
        nuevo_dia = request.get_json()
        if 'dia_numero' in nuevo_dia and 'hora_inicio' in nuevo_dia and 'hora_fin' in nuevo_dia and 'id_medico' in nuevo_dia:
            agenda_formateada = modifcar_dia_de_atencion(nuevo_dia['dia_numero'], nuevo_dia['hora_inicio'], nuevo_dia['hora_fin'], id_medico)
            return agenda_formateada, 201
        else:
            return jsonify({'error': 'Datos incorrectos'}), 400
    else:
        return jsonify({'error': 'No se recibió información en formato JSON'}), 400
    
@agenda_bp.route('/agenda_medicos/<id_medico>', methods=['DELETE'])
def eliminar_dia(id_medico):
    if request.is_json:
        eliminar_dia = request.get_json()
        if 'dia_numero' in eliminar_dia and 'hora_inicio' in eliminar_dia and 'hora_fin' in eliminar_dia and 'id_medico' in eliminar_dia:
            agenda_formateada = eliminar_dia_horario(eliminar_dia['dia_numero'], eliminar_dia['hora_inicio'], eliminar_dia['hora_fin'], id_medico)
            return agenda_formateada, 201
        else:
            return jsonify({'error': 'Datos incorrectos'}), 400
    else:
        return jsonify({'error': 'No se recibió información en formato JSON'}), 400
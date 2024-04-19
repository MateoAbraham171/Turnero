from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_por_id_medico, obtener_turnos_pendientes_por_id_medico, obtener_turno_por_id_paciente, eliminar_turno_por_id, agendar_turno, turno_en_menos_de_30_dias, turno_disponible, turno_cada_quince
from modelos.medicos import chequear_medico_habilitado
from modelos.agenda_medicos import dia_que_trabaja, hora_que_trabaja

turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
def obtener_turnos_por_id(id):
    turnos = obtener_turnos_por_id_medico(id)
    if len(turnos) > 0:
        return jsonify(turnos), 200
    else:
        return jsonify({'message': 'No hay turnos de este médico'}), 404

@turnos_bp.route('/turnos_pendientes/<int:id>', methods=['GET'])
def obtener_turnos_pendientes(id):
    turnos_pendientes = obtener_turnos_pendientes_por_id_medico(id)
    if len(turnos_pendientes) > 0:
        return jsonify(turnos_pendientes), 200
    else:
        return jsonify({'message': 'No hay turnos pendientes de este médico'}), 404

@turnos_bp.route('/turnos', methods=['POST'])
def agregar_turno():
    if request.is_json:
        turno = request.get_json()
        if 'id_medico' in turno and 'id_paciente' in turno and 'hora_turno' in turno and 'fecha_solicitud' in turno:
            if turno_en_menos_de_30_dias(turno['fecha_solicitud']):
                if turno_cada_quince(turno['hora_turno']):
                    if chequear_medico_habilitado(turno['id_medico']):
                        dia = dia_que_trabaja(turno['id_medico'], turno['fecha_solicitud'])
                        if dia:
                            if hora_que_trabaja(dia, turno['hora_turno'], turno['id_medico']):
                                if turno_disponible(turno['id_medico'], turno['hora_turno']):
                                    return jsonify({agendar_turno(turno): 'Turno creado exitosamente!'}), 201
                                else:
                                    return jsonify({'message': 'Este turno no se encuentra disponible'}), 400
                            else:
                                return jsonify({'message': 'El medico no trabaja en el horario solicitado'}), 400
                        else:
                            return jsonify({'message': 'El medico no trabaja en el día solicitado'}), 400
                    else:
                        return jsonify({'message': 'El medico no esta habilitado'}), 400
                else:
                    return jsonify({'message': 'El turno debe ser en los minutos "00"-"15"-"30"-"45"'}), 400
            else:
                return jsonify({'message': 'El turno debe ser en menos de 30 días'}), 400
        else:
            return jsonify({'error': 'Faltan datos'}), 400
    else:
        return jsonify({'error': 'No se ha recibido un JSON válido'}), 400
                                        
@turnos_bp.route('/turnos/<int:id>', methods=['DELETE'])
#debe ingresas id_paciente
def registrar_anulacion_turno(id):
    if obtener_turno_por_id_paciente(id):
        eliminar_turno_por_id(id)
        return jsonify({'message': 'Turno eliminado correctamente'}), 200
    else:
        return jsonify({'message': 'No se ha encontrado el turno'}), 404
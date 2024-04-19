import csv
import requests
from modelos.medicos import obtener_medico_por_id
from modelos.pacientes import obtener_paciente_por_id
from modelos.agenda_medicos import obtener_agenda_ordenada
import datetime

# Variables globales que usaremos en este módulo
turnos = []
ruta_archivo_turnos = 'turnos.csv'

def inicializar_turnos():
    """
    Inicializa la lista de turnos mediante la API.
    """
    global turnos
    global id_medico
    url = 'https://randomuser.me/api/?inc=registered,dob&noinfo&nat=es&results=300'
    response = requests.get(url)
    datos = response.json()['results']
    if response.status_code == 200:
        meter_turnos_en_lista(datos)

def meter_turnos_en_lista(datitos):
    # Definir la lista de turnos dentro de la función
    global turnos
    agenda_medicos = obtener_agenda_ordenada()

    for persona in datitos:
        # Obtener la fecha y hora del JSON
        date_str = persona["registered"]["date"]
        date_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        # Obtener los componentes de la fecha y hora
        year, month, day = date_obj.year, date_obj.month, date_obj.day
        hour, minute = date_obj.hour, date_obj.minute

        # Formatear los minutos a dos dígitos
        minute = f'{minute:02d}'

        turno_a_agregar = {
            "id_medico": persona["dob"]["age"],
            "id_paciente": persona["registered"]["age"],
            "hora_turno": f'{hour:02d}:{minute}',
            "fecha_solicitud": f'{month:02d}-{day:02d}'
        }

        # Verificar que el turno sea con separación cada 15 minutos
        if int(minute) % 15 == 0:
            # Verificar la existencia del paciente y del médico
            if obtener_paciente_por_id(turno_a_agregar["id_paciente"]) and obtener_medico_por_id(turno_a_agregar["id_medico"]):
                numero_dia_semana = date_obj.weekday()

                # Filtrar los días que atiende el médico por su ID
                dias_que_atiende = [linea for linea in agenda_medicos if linea["id_medico"] == turno_a_agregar["id_medico"]]

                for medico in dias_que_atiende:
                    if medico["dia_numero"] == numero_dia_semana:
                        hora_inicio = datetime.datetime.strptime(medico["hora_inicio"], '%H:%M').time()
                        hora_fin = datetime.datetime.strptime(medico["hora_fin"], '%H:%M').time()
                        hora_turno = datetime.datetime.strptime(turno_a_agregar["hora_turno"], '%H:%M').time()

                        # Verificar si la hora está dentro del rango
                        if hora_inicio <= hora_turno <= hora_fin:
                            turnos.append(turno_a_agregar)

    # Exportar la lista completa de turnos después de haber procesado todos los datos
    exportar_a_csv(turnos)
            
def exportar_a_csv():
    global pacientes
    with open(ruta_archivo_turnos, 'w', newline='', encoding='utf8') as csvfile:
        campo_nombres = ['id_medico','id_paciente','hora_turno','fecha_solicitud']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for turno in turnos:
            writer.writerow(turno)

def obtener_turnos_por_id_medico(id_medico):
    """
    Obtiene los turnos de un médico en particular.
    """
    global turnos
    return [turno for turno in turnos if turno['id_medico'] == id_medico]

def obtener_turnos_pendientes_por_id_medico(id_medico):
    turnos_pendientes = []

    for turno in turnos:
        if turno['id_medico'] == id_medico:
            fecha_hoy = datetime.date.today()
            fecha_turno = turno["fecha_solicitud"]
            
            # Comparar solo las partes de la fecha
            if fecha_hoy < datetime.datetime.strptime(fecha_turno, '%m-%d').date():
                turnos_pendientes.append(turno)
                
    if len(turnos_pendientes)>0:
        return turnos_pendientes
    else:
        return None
    
def turno_cada_quince(hora_turno):
    """
    Verifica si un turno se puede programar cada 15 minutos.
    """
    hora, minuto = hora_turno.split(":")
    hora = int(hora)
    minuto = int(minuto)
    if minuto % 15 == 0:
        return True
    else:
        return False
    
def turno_en_menos_de_30_dias(fecha_solicitud):
    """
    Verifica si un turno está en menos de 30 días.
    """
    fecha_hoy = datetime.date.today()
    fecha_turno = datetime.datetime.strptime(fecha_solicitud, '%m-%d').date()
    if fecha_hoy - fecha_turno <= datetime.timedelta(days=30):
        return True
    else:
        return False
     
def turno_disponible(id_medico, hora_turno):
    """
    Verifica si un turno está disponible para un médico en particular.
    """
    global turnos
    turnos_medico = obtener_turnos_pendientes_por_id_medico(id_medico)
    for turno in turnos_medico:
        if turno['hora_turno'] == hora_turno:
            return False
    return True

def agendar_turno(id_medico, id_paciente, hora_turno, fecha_solicitud):
    turno_a_agregar ={
        "id_medico": id_medico,
        "id_paciente": id_paciente,
        "hora_turno": hora_turno,
        "fecha_solicitud": fecha_solicitud
    }
    turnos.append(turno_a_agregar)
    exportar_a_csv()
    return turnos[-1]

def obtener_turno_por_id_paciente(id_paciente):
    global turnos
    turno_a_buscar = [turno for turno in turnos if turno['id_paciente'] == id_paciente]
    if len(turno_a_buscar) > 0:
        return turno_a_buscar[0]
    else:
        return None

def eliminar_turno_por_id(id_paciente):
    global turnos
    turno_a_eliminar = [turno for turno in turnos if turno['id_paciente'] == id_paciente]
    turnos.remove(turno_a_eliminar[0])
    exportar_a_csv()
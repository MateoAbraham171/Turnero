import csv
import os
import datetime

lista_agenda = []
ruta_archivo = 'agenda_medicos.csv'

def inicializar_agenda():
    if os.path.exists(ruta_archivo):
        importar_datos_desde_csv()

def importar_datos_desde_csv():
    global lista_agenda
    lista_agenda = []
    with open(ruta_archivo, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id_medico'] = int(row['id_medico'])
            row['dia_numero'] = int(row['dia_numero'])
            row['hora_inicio'] = datetime.datetime.strptime(row['hora_inicio'], '%H:%M')
            row['hora_fin'] = datetime.datetime.strptime(row['hora_fin'], '%H:%M')
            lista_agenda.append(row)

def guardar_en_csv():
    with open("agenda_medicos.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_agenda[0].keys()
        csv_writer.writerow(header)

        for row in lista_agenda:
            csv_writer.writerow(row.values())

def obtener_agenda_ordenada():
    global lista_agenda
    lista_medicos_ordenada = sorted(lista_agenda, key=lambda x: x['id_medico'])
    for id in lista_agenda:
        lista_medicos_ordenada = sorted(lista_agenda[id], key=lambda x: x['dia_numero'])
        lista_medicos_ordenada = sorted(lista_medicos_ordenada[id], key=lambda x: x['hora_inicio'])
    print(lista_medicos_ordenada)

def agregar_dia_horario(dia, horario_inicio, horario_fin, id_medico):
    global lista_agenda
    if dia.strftime('%w') in ['0', '1', '2', '3', '4', '5', '6']:
        if horario_inicio < horario_fin:
            lista_agenda.append({
                'id_medico': id_medico,
                'dia_numero': dia,
                'hora_inicio': horario_inicio,
                'hora_fin': horario_fin
            })
            guardar_en_csv()
        else:
            #print("El horario de inicio debe ser menor que el de fin")
            return None
    else:
        #print("El día debe ser un día de la semana")
        return None
    guardar_en_csv()
    return lista_agenda[-1]

def modifcar_dia_de_atencion(dia, hora_inicio_nuevo, hora_fin_nuevo, id_medico):
    global lista_agenda
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if dia.strftime('%w') in ['0', '1', '2', '3', '4', '5', '6']:
                if hora_inicio_nuevo < hora_fin_nuevo:
                    if agenda['dia_numero'] == dia:
                        agenda['hora_inicio'] = hora_inicio_nuevo
                        agenda['hora_fin'] = hora_fin_nuevo
                        guardar_en_csv()

                        return lista_agenda[-1]
                else:
                    #print("El horario de inicio debe ser menor que el de fin")
                    return None
            else:
                #print("El día debe ser un día de la semana")
                return None

def eliminar_dia_horario(dia, hora_inicio, hora_fin, id_medico):
    global lista_agenda
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == dia:
                if agenda['hora_inicio'] == hora_inicio and agenda['hora_fin'] == hora_fin:
                    lista_agenda.remove(agenda)
                    guardar_en_csv()
                    return lista_agenda[-1]
    return None

def dia_que_trabaja(id_medico, fecha_solicitud):
    global lista_agenda
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == fecha_solicitud.strftime('%w'):
                return agenda['dia_numero']
    return None

def hora_que_trabaja(dia, hora_buscada, id_medico):
    global lista_agenda
    for agenda in lista_agenda:
        if agenda['id_medico'] == id_medico:
            if agenda['dia_numero'] == dia:
                hora_buscada = datetime.datetime.strptime(hora_buscada, '%H:%M').time()
                hora_inicio = datetime.datetime.strptime(agenda['hora_inicio'], '%H:%M').time()
                hora_fin = datetime.datetime.strptime(agenda['hora_fin'], '%H:%M').time()
                if hora_buscada >= hora_inicio and hora_buscada <= hora_fin:
                    return True
    return False
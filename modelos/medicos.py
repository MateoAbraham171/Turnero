import csv
import requests
id_medico = 0
lista_medicos = []

def iniciar_medicos():
    url = "https://randomuser.me/api/?results=15&inc=name,email,phone,id,login&exc=registered,location,picture,dob,gender&noinfo&password=upper,lower,6-6&nat=es"
    response = requests.get(url)
    datos = response.json()['results']
    if response.status_code == 200:
        tomar_datos_medicos(datos)

def tomar_datos_medicos(data):
    global id_medico
    global lista_medicos
    
    for user in data:
        if user['id']['value']:
            medico_formateado = {
                'id': id_medico + 1,
                'dni': user['id']['value'],
                'nombre': user['name']['first'],
                'apellido': user['name']['last'],
                'telefono': user['phone'],
                'matricula': user['login']['password'],
                'email': user['email'],
                'habilitado': "si"
            }
            lista_medicos.append(medico_formateado)
            id_medico += 1
    guardar_en_csv()

def guardar_en_csv():
    with open("medicos.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_medicos[0].keys()
        csv_writer.writerow(header)

        for row in lista_medicos:
            csv_writer.writerow(row.values())

def crear_medico(dni, nombre, apellido, telefono, matricula, email):
    global id_medico
    # Agrega el médico a la lista con un ID único
    lista_medicos.append({
        'id': id_medico+1,
        'dni': dni,
        'nombre': nombre,
        'apellido':apellido,
        'telefono': telefono,
        'matricula':matricula,
        'email': email,
        'habilitado': "si"
    })
    id_medico += 1
    guardar_en_csv()
    # Devuelve el médico recién creado
    return lista_medicos[-1]

def obtener_medico_por_id(id):
    # Recorre la lista de médicos
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve el médico
        if medico["id"] == id:
            return medico
    # Devuelve None si no se encuentra el médico
    return None

def obtener_medicos():
    return lista_medicos

def editar_medico_por_id(id, dni, nombre, apellido, telefono, matricula, email,):
    # Recorre la lista de médicos
    for medico in lista_medicos:
        if medico["id"] == id:
            medico['dni'] = dni
            medico['nombre'] = nombre
            medico['apellido'] = apellido
            medico['telefono'] = telefono
            medico['matricula'] = matricula
            medico['email'] = email
            guardar_en_csv()  # Asumo que esta función guarda la lista actualizada en un archivo CSV
            return medico
    # Devuelve None si no se encuentra el médico
    return None

def existe_medico(id):
    # Recorre la lista de médicos
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve True
        if medico["id"] == id:
            return True
    # Devuelve False si no se encuentra el médico
    return False

def deshabilitar_medico (id):
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve True
        if medico["id"] == id:
           medico["habilitado"] = "no"
           return medico
    # Devuelve False si no se encuentra el médico
    return False

def chequear_medico_habilitado(id):
    for medico in lista_medicos:
        # Si el ID del médico coincide, devuelve True
        if medico["id"] == id:
           if medico["habilitado"] == "si":
               return True
           else:
               return False
    # Devuelve False si no se encuentra el médico
    return False
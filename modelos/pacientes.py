import csv
import requests

id_paciente = 0
lista_pacientes = []

def iniciar_pacientes():
    global id_paciente
    url = "https://randomuser.me/api/?results=5&inc=name,email,location,phone,id,login&exc=registered,picture,dob,gender&noinfo&nat=es"
    response = requests.get(url)
    datos = response.json()['results']
    if response.status_code == 200:
        tomar_datos_pacientes(datos)

def tomar_datos_pacientes(data):
    global id_paciente
    global lista_pacientes
    
    for user in data:
        if user['id']['value']:
            paciente_formateado = {
                'id': id_paciente + 1,
                'dni': user['id']['value'],
                'nombre': user['name']['first'],
                'apellido': user['name']['last'],
                'telefono': user['phone'],
                'email': user['email'], 
                'direccion_calle': user['location']['street']['name'],
                'direccion_numero': user['location']['street']['number'],
            }
            lista_pacientes.append(paciente_formateado)
            id_paciente += 1
    guardar_en_csv()

def guardar_en_csv():
    with open("pacientes.csv", "w", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        header = lista_pacientes[0].keys()
        csv_writer.writerow(header)

        for row in lista_pacientes:
            csv_writer.writerow(row.values())

def crear_paciente(dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    global id_paciente
    # Agrega al paciente a la lista con un ID único
    lista_pacientes.append({
        'id': id_paciente + 1,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'direccion_calle': direccion_calle,
        'direccion_numero': direccion_numero,
        'habilitado': "si"
    })
    id_paciente += 1
    guardar_en_csv()
    # Devuelve el paciente recién creado
    return lista_pacientes[-1]

def obtener_paciente_por_id(id):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        # Si el ID del paciente coincide, devuelve el paciente
        if paciente["id"] == id:
            return paciente
    # Devuelve None si no se encuentra el paciente
    return None

def obtener_pacientes():
    return lista_pacientes

def editar_paciente_por_id(id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        if paciente["id"] == id:
            paciente['dni'] = dni
            paciente['nombre'] = nombre
            paciente['apellido'] = apellido
            paciente['telefono'] = telefono
            paciente['email'] = email
            paciente['direccion_calle'] = direccion_calle
            paciente['direccion_numero'] = direccion_numero
            guardar_en_csv()
            return paciente
    # Devuelve None si no se encuentra el paciente
    return None

def existe_paciente(id):
    # Recorre la lista de pacientes
    for paciente in lista_pacientes:
        # Si el ID del paciente coincide, devuelve True
        if paciente["id"] == id:
            return True
    # Devuelve False si no se encuentra el paciente
    return False

def eliminar_paciente_por_id(id):
    global lista_pacientes
    # Crea una nueva lista sin el paciente a eliminar
    paciente_a_eliminar = [paciente for paciente in lista_pacientes if paciente["id"] == id]
    if len(paciente_a_eliminar) > 0:
        lista_pacientes.remove(paciente_a_eliminar[0])
        guardar_en_csv() 
        return paciente_a_eliminar[0]
    else:
        return None

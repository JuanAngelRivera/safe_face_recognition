import os
import numpy as np
from source.utils.connection import connect

def load_user(nombre):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute('select id_usuario from usuario where autorizado = true and nombre = %s;', (nombre, ))
    usuario = cursor.fetchone()
    id_usuario = usuario[0]

    encoding_path = (f'storage/users/{id_usuario}/encoding.npy')

    if os.path.exists(encoding_path):
        encoding = np.load(encoding_path)

    if encoding is None:
        print('No se encontró el encoding')
        exit()

    return encoding, id_usuario

def get_admin(nombre):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute('select 1 from usuario where autorizado = true and nombre = %s and administrador = true;', (nombre, ))
    verification = cursor.fetchone()

    return verification[0] == 1



def load_users():
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute('select id_usuario, nombre from usuario where autorizado = true;')
    usuarios = cursor.fetchall()

    known_encodings = []
    known_names = []
    known_ids = []

    for usuario in usuarios:
        id_usuario = usuario[0]
        nombre = usuario[1]

        encoding_path = (f'storage/users/{id_usuario}/encoding.npy')

        if os.path.exists(encoding_path):
            encoding = np.load(encoding_path)
            known_encodings.append(encoding)
            known_names.append(nombre)
            known_ids.append(id_usuario)

    if len(known_encodings) == 0:
        print('No hay usuarios registrados')
        exit()

    print('Usuarios cargados:', len(known_encodings))
    return known_encodings, known_names, known_ids
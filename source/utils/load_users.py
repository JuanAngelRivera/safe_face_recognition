import os
import numpy as np
from source.arduino.main.utils.connection import connect

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
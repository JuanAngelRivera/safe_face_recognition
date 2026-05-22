import os
import numpy as np
import psycopg
from dotenv import load_dotenv

load_dotenv()

def load_users():
    connection = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT')
    )
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
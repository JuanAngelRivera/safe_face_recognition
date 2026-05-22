import psycopg
import os
from dotenv import load_dotenv

def save_log(id_usuario, autorizado, confianza):
    load_dotenv()
    
    connection = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT')
    )

    cursor = connection.cursor()
    cursor.execute(
        'insert into acceso (id_usuario, autorizado, confianza) values (%s, %s, %s);',
        (id_usuario, autorizado, confianza))
    
    connection.commit()
    cursor.close()
    connection.close()
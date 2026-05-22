import psycopg

def save_log(id_usuario, autorizado, confianza):
    connection = psycopg.connect(
        dbname = 'safe_face_recognition',
        user = 'administrador',
        password = '123',
        host = '127.0.0.1'
    )

    cursor = connection.cursor()
    cursor.execute(
        'insert into acceso (id_usuario, autorizado, confianza) values (%s, %s, %s);',
        (id_usuario, autorizado, confianza))
    
    connection.commit()
    cursor.close()
    connection.close()
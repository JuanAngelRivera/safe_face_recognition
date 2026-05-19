import psycopg

conn = psycopg.connect(
    host = '127.0.0.1',
    dbname = 'safe_face_recognition',
    user = 'administrador',
    password = '123',
    port = 5432,
)

cur = conn.cursor()

usuarios = cur.execute('select * from usuario').fetchall()

if usuarios:
    for usuario in usuarios:
        print(usuario)
else:
    print('No hay usuarios!')
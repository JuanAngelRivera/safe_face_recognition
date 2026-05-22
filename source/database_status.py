import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        host = os.getenv('HOST'),
        port = os.getenv('PORT')
    )

cursor = connection.cursor()

print("\n=========================")
print("USUARIOS REGISTRADOS")
print("=========================\n")

cursor.execute("""
    SELECT
        id_usuario,
        nombre,
        autorizado,
        fecha_registro
    FROM usuario
    ORDER BY id_usuario
""")

usuarios = cursor.fetchall()

if len(usuarios) == 0:
    print("No hay usuarios registrados\n")

else:

    for usuario in usuarios:

        print(f"""
ID: {usuario[0]}
Nombre: {usuario[1]}
Autorizado: {usuario[2]}
Fecha Registro: {usuario[3]}
-----------------------------
""")

print("\n=========================")
print("LOGS DE ACCESO")
print("=========================\n")

cursor.execute("""
    SELECT
        a.id_acceso,
        u.nombre,
        a.fecha,
        a.autorizado,
        a.confianza
    FROM acceso a
    LEFT JOIN usuario u
        ON a.id_usuario = u.id_usuario
    ORDER BY a.fecha DESC
""")

accesos = cursor.fetchall()

if len(accesos) == 0:
    print("No hay registros de acceso\n")
else:
    for acceso in accesos:
        nombre = acceso[1]

        if nombre is None:
            nombre = "DESCONOCIDO"

        print(f"""
            ID Acceso: {acceso[0]}
            Usuario: {nombre}
            Fecha: {acceso[2]}
            Autorizado: {acceso[3]}
            Confianza: {acceso[4]}
            -----------------------------
            """)
        
cursor.close()
connection.close()

from source.arduino.main.utils.connection import connect

connection = connect()
cursor = connection.cursor()

print("\n=========================")
print("USUARIOS REGISTRADOS")
print("=========================\n")

cursor.execute(
    '''
        select id_usuario, nombre, autorizado, fecha_registro
        from usuario
        order by 1;
    ''')

usuarios = cursor.fetchall()

if len(usuarios) == 0:
    print("No hay usuarios registrados\n")

else:
    for usuario in usuarios:
        print(
            f"""
                ID: {usuario[0]}
                Nombre: {usuario[1]}
                Autorizado: {usuario[2]}
                Fecha Registro: {usuario[3]}
                -----------------------------
            """)

print("\n=========================")
print("LOGS DE ACCESO")
print("=========================\n")

cursor.execute(
    '''
        select a.id_acceso, u.nombre, a.fecha, a.autorizado, a.confianza
        from acceso a
        left outer join usuario u on a.id_usuario = u.id_usuario
        order by a.fecha;
    ''')

accesos = cursor.fetchall()

if len(accesos) == 0:
    print("No hay registros de acceso\n")
else:
    for acceso in accesos:
        nombre = acceso[1]

        if nombre is None:
            nombre = "DESCONOCIDO"

        print(
            f"""
                ID Acceso: {acceso[0]}
                Usuario: {nombre}
                Fecha: {acceso[2]}
                Autorizado: {acceso[3]}
                Confianza: {acceso[4]}
                -----------------------------
            """)
        
cursor.close()
connection.close()
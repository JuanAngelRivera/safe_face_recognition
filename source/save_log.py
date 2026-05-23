from connection import connect
def save_log(id_usuario, autorizado, confianza): 
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        '''
            insert into acceso (id_usuario, autorizado, confianza)values 
            (%s, %s, %s);
        ''', (id_usuario, autorizado, confianza))
    
    connection.commit()
    cursor.close()
    connection.close()
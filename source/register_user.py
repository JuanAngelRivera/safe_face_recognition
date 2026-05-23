import cv2
import face_recognition
import numpy as np
import os
import config
from connection import connect

nombre = input('Nombre de usuario: ')

connection = connect()

cursor = connection.cursor()
cursor.execute('insert into usuario(nombre) values (%s) returning id_usuario;', (nombre, ))

id_usuario = cursor.fetchone()[0]
print('id usuario:', id_usuario)

connection.commit()

user_folder = f'storage/users/{id_usuario}'
os.makedirs(user_folder, exist_ok = True)

camera_source = config.camera_source

if camera_source.isdigit():
    camera_source = int(camera_source)

capture = cv2.VideoCapture(camera_source)

print('Presiona \'ESPACIO\'para capturar foto')

while True:
    ret, frame = capture.read()
    cv2.imshow('Registro', frame)
    key = cv2.waitKey(1)

    if key == 32:
        break

capture.release()
cv2.destroyAllWindows()

image_path = f'{user_folder}/profile.jpg'
cv2.imwrite(image_path, frame)

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

encodings = face_recognition.face_encodings(rgb)

if len(encodings) == 0:
    print('No se detectó un rostro')
    exit()

encoding = encodings[0]

np.save(f'{user_folder}/encoding.npy', encoding)
print('Usuario registrado correctamente')   
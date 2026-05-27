import cv2
import face_recognition
import numpy as np
import os
from source.utils.config import camera_source as cm
from source.utils.connection import connect

def register_user(nombre):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('insert into usuario(nombre) values (%s) returning id_usuario;', (nombre, ))

    id_usuario = cursor.fetchone()[0]
    print('id usuario:', id_usuario)

    connection.commit()

    user_folder = f'storage/users/{id_usuario}'
    os.makedirs(user_folder, exist_ok = True)

    camera_source = cm

    if camera_source.isdigit():
        camera_source = int(camera_source)

    capture = cv2.VideoCapture(camera_source)

    frame_count = 0
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        frame_count += 1

        display_frame = frame.copy()

        if frame_count % 15 == 0:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb, model = 'hog')
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            if len(face_encodings) == 0:
                continue
                
            image_path = f'{user_folder}/profile.jpg'
            cv2.imwrite(image_path, frame)

            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) == 0:
                print('No se detectó un rostro')
                exit()

            encoding = encodings[0]

            np.save(f'{user_folder}/encoding.npy', encoding)
            print('Usuario registrado correctamente')
            return True
        
        cv2.imshow("Register user", display_frame)
        if cv2.waitKey(1) & 0xFF == 32:
            break
        
    capture.release()
    cv2.destroyAllWindows()

    return False
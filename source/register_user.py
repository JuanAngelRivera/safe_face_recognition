import face_recognition
import numpy as np
import os

image_path = 'datos_prueba/face.jpg'

image = face_recognition.load_image_file(image_path)

encodings = face_recognition.face_encodings(image)

if len(encodings) == 0:
    print('No se detectó ningún rostro')
    exit
print(encodings)
encoding = encodings[0]

os.makedirs('storage/users/cherry', exist_ok = True)

np.save('storage/users/cherry/encoding.npy', encoding)

print('Embedding guardado correctamente')
print(np.load('storage/usets/cherry/encoding.npy'))
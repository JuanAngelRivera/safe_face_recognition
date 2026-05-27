import cv2
import face_recognition
import numpy as np
import os
import source.utils.config as config
from dotenv import load_dotenv
from source.utils.esp32_controller import ( open_access, deny_access)

load_dotenv()

def recognize_user(nombre):
    embedding_path = os.path.join("storage", "embeddings", f"{nombre}.npy")

    if not os.path.exists(embedding_path):
        print("Embedding no encontrado")
        return False

    known_encoding = np.load(embedding_path)
    camera_source = config.camera_source
    print(camera_source)

    if camera_source.isdigit():
        camera_source = int(camera_source)

    capture = cv2.VideoCapture(camera_source)

    if not capture.isOpened():
        print("Error: No se pudo acceder a la cámara")
        return False

    print("Verificando identidad...")
    max_intentos = 30  # Detiene el bucle tras ~30 cuadros analizados si nadie aparece
    intentos = 0

    while intentos < max_intentos:
        ret, frame = capture.read()
        if not ret:
            break

        intentos += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model='hog')
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for face_encoding in face_encodings:
            distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
            print(f"Distancia calculada: {distance}")

            if distance < 0.5:
                print("ACCESO CONCEDIDO")
                open_access()
                capture.release()
                cv2.destroyAllWindows()
                return True
            else:
                print("ACCESO DENEGADO")
                deny_access()

        # Nota: cv2.imshow puede fallar o congelarse dentro de hilos de Flask. 
        # Si te da problemas en entornos web, puedes comentar las siguientes 3 líneas:
        cv2.imshow("Verificacion Facial", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
    print("Tiempo de espera agotado / Rostro no reconocido")
    return False

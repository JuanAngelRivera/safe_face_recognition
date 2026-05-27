import cv2
import face_recognition
import numpy as np
from source.utils.load_users import load_users
from source.utils.save_log import save_log
import source.utils.config as config

known_encodings, known_names, known_ids = load_users()
print(known_names)

camera_source = config.camera_source

if camera_source.isdigit():
    camera_source = int(camera_source)

capture = cv2.VideoCapture(camera_source)
frame_count = 0
last_detected_name = None

if len(known_encodings) == 0:
    print("No hay usuarios registrados")
    exit()
    
while True:
    ret, frame = capture.read()

    if not ret:
        break

    frame_count += 1
    display_frame = frame.copy()

    if frame_count % 30 == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model='hog')
        face_encodings = face_recognition.face_encodings(rgb, face_locations)
    if len(face_encodings) == 0:
        last_detected_name = None

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            distance = face_distances[best_match_index]

            if distance < config.face_match_threshold:
                label = known_names[best_match_index]
                id_usuario = known_ids[best_match_index]
                autorizado = True
                color = (0, 255, 0)
                
                print('Reconocido :3c')
                #requests.get(f"{ESP32_URL}/open")
                open_access()
                
            else:
                label = 'Desconocido'
                id_usuario = None
                autorizado = False
                color = (0, 0, 255)
                print('No reconocido >:3')
                #requests.get(f"{ESP32_URL}/deny")
                deny_access()

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if label != last_detected_name:
                save_log(id_usuario, autorizado, float(distance))
                last_detected_name = label

                print('log guardado:', label)

            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
            cv2.putText(display_frame, f'{label} {distance:.2f}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Recognition", display_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
cv2.destroyAllWindows()


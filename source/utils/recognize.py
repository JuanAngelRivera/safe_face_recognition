import cv2
import face_recognition
import numpy as np
from source.utils.load_users import load_user
from source.utils.save_log import save_log
import source.utils.config as config
from source.utils.esp32_controller import open_access, deny_access

def recognize(encoding, id):
    camera_source = config.camera_source

    if camera_source.isdigit():
        camera_source = int(camera_source)

    capture = cv2.VideoCapture(camera_source)
    print('Encendió cámara')
    attempts = 0
    max_attempts = 150
    failed_attempt = 0

    while attempts < max_attempts and failed_attempt < 3:
        ret, frame = capture.read()

        if not ret:
            break

        attempts += 1
        display_frame = frame.copy()

        if attempts % 15 == 0:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb, model = 'hog')
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            if len(face_encodings) == 0:
                continue

            for face_location, face_encoding in zip(face_locations, face_encodings):

                face_distance = face_recognition.face_distance([encoding], face_encoding)
                distance = face_distance[0]

                if distance < float(config.face_match_threshold):  
                    print('Reconocido :3c')
                    open_access() 
                    save_log(id, True, distance)
                    return True
                else:
                    failed_attempt += 1
                    print('No reconocido >:3:', failed_attempt)
                    deny_access()
                    save_log(id, False, distance)
                
        cv2.imshow("Recognition", display_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

    return False
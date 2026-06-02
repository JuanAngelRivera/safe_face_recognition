import cv2
import face_recognition
import numpy as np
from source.utils.load_users import load_users
from source.utils.save_log import save_log
import source.utils.config as config
from source.utils.esp32_controller import open_access, deny_access
import time
import threading

known_encodings, known_names, known_ids = load_users()
cv2.setUseOptimized(True)
cv2.setNumThreads(4)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

latest_frame = None
frame_lock = threading.Lock()

tracked_faces = []
faces_lock = threading.Lock()

running = True
last_detected_name = None

def camera_thread():
    global latest_frame, running

    while running:
        ret, frame = capture.read()

        if not ret:
            continue
    
        with frame_lock:
            latest_frame = frame.copy()

def recognition_thread():
    global tracked_faces
    global last_detected_name

    process_every = 1

    while running:
        with frame_lock:
            if latest_frame is None:
                continue
            
            frame = latest_frame.copy()

        small_frame = cv2.resize(frame, (0, 0), fx = 0.2, fy = 0.2)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model = 'hog')
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        current_faces = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            distance = face_distances[best_match_index]

            if distance < float(config.face_match_threshold):
                label = known_names[best_match_index]
                id_usuario = known_ids[best_match_index]
                color = (0, 255, 0)

                print('Reconocido :3c')

                if label != last_detected_name:
                    open_access()
                    save_log(id_usuario, True, float(distance))
                    last_detected_name = label   
            else:
                label = 'Desconocido'
                color = (0, 0, 255)
                print('No reconocido >:3')

                if label != last_detected_name:
                    deny_access()
                    save_log(None, False, float(distance))
                    last_detected_name = label

            scale = 5
            top *= scale
            left *= scale
            bottom *= scale
            right *= scale
            
            current_faces.append({
                "top": top,
                "right": right,
                "bottom": bottom,
                "left": left,
                "label": label,
                "distance": distance,
                "color": color
                })
            
        with faces_lock:
            tracked_faces = current_faces
        
        time.sleep(process_every)

threading.Thread(
    target = camera_thread,
    daemon = True
).start()

threading.Thread(
    target = recognition_thread,
    daemon = True
).start()


while True:
    with frame_lock:
        if latest_frame is None:
            continue

        display_frame = latest_frame.copy()

    with faces_lock:
        for face in tracked_faces:
            cv2.rectangle(
                display_frame,
                (face['left'], face['top']),
                (face['right'], face['bottom']),
                face['color'],
                2
            )

            cv2.putText(
                display_frame,
                f"{face['label']} {face['distance']:.2f}",
                (face['left'], face['top'] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                face['color'],
                2
            )

    cv2.imshow('Safe recognition', display_frame)

    if cv2.waitKey(1) & 0xFF == 32:
        running = False
        break

capture.release()
cv2.destroyAllWindows()

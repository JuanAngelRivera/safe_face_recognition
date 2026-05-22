import cv2
import face_recognition
import numpy as np
from load_users import load_users

known_encodings, known_names, known_ids = load_users()
print(known_names)

cap = cv2.VideoCapture(0)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    display_frame = frame.copy()

    if frame_count % 30 == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb, model='hog')
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            distance = face_distances[best_match_index]

            if distance < 0.5:
                label = known_names[best_match_index]
                color = (0, 255, 0)
            else:
                label = 'Desconocido'
                color = (0, 0, 255)

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
            cv2.putText(display_frame, f'{label} {distance:.2f}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Recognition", display_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import face_recognition
import numpy as np

known_encoding = np.load(
    "storage/users/cherry/encoding.npy"
)

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
        face_encodings = face_recognition.face_encodings(rgb,face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([known_encoding], face_encoding)

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if matches[0]:
                label = "AUTORIZADO"
                color = (0, 255, 0)
            else:
                label = "DENEGADO"
                color = (0, 0, 255)

            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
            cv2.putText(display_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Recognition", display_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
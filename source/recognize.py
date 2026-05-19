import cv2
import face_recognition
import numpy as np

known_encoding = np.load('storage/users/cherry/encoding.npy')

capture = cv2.VideoCapture(1)

while True:
    ret, frame = capture.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        distance = face_recognition.face_distance([known_encoding], face_encoding)[0]

        if matches[0]:
            label = f'AUTORIZADO {distance:.2f}'
            color = (0, 255, 0)
        else:
            label = f'DENEGADO {distance:.2f}'
            color = (0, 0, 255)

    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.imshow('Recognition', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
cv2.destroyAllWindows()
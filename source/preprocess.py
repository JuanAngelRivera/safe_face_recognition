import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    if len(faces) > 0:
        (x, y, w, h) = faces[0]

        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        cv2.imwrite(f"datos_prueba/face.jpg", face)

cap.release()
cv2.destroyAllWindows()
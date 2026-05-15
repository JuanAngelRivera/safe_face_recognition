import cv2

cam = cv2.VideoCapture(0)

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

while True:

    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

    cv2.imshow("Deteccion Facial", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
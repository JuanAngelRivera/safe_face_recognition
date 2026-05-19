import cv2


cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    if not ret:
        print('No ret')
        break

    cv2.imshow("DroidCam IP", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

print('fuera del bucle')
cap.release()
cv2.destroyAllWindows()
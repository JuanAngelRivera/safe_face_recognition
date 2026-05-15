import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Resize
    frame = cv2.resize(frame, (640, 480))

    # 2. Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 3. Mejora de contraste
    gray = cv2.equalizeHist(gray)

    cv2.imshow("Original", frame)
    cv2.imshow("Procesado", gray)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
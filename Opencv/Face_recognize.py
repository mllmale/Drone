import cv2

video = cv2.VideoCapture(0)

while True:
    _, img = video.read()
    cv2.imshow("detecção de face", img)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("detecção de face", cv2.WND_PROP_VISIBLE) < 1:
        break

video.release()
cv2.destroyAllWindows()
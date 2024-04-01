import cv2
import cvzone

fpsReader = cvzone.FPS(avgCount=30)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    success, img = cap.read()
    fps, img = fpsReader.update(img, pos=(20, 50),
                                bgColor=(255, 0, 255), textColor=(255,255,255),
                                scale=3, thickness=3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("detecção de face", cv2.WND_PROP_VISIBLE) < 1:
        break
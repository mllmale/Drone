import cv2
import cvzone

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 100, 150)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgList = [img, imgGray, imgCanny, imgHSV]
    stackedImg = cvzone.stackImages(imgList, 2, 0.7)

    cv2.imshow("tudo", stackedImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



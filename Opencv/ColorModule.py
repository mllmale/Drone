import cv2
import numpy as np
import cvzone

"""
hsv -> sistemas de cores formadas por Hue (matriz), saturação e value 
    hue (tonalidade) -> tipo de cor, abrangendo um espectro
    saturação -> quanto menor o valor, mais próximo de cinza será a img
    valor -> define o brilho 
"""
# Define um range para a busca de uma tonalidade
lower = np.array([35, 50, 50])  # h = 15, s = 150, v = 20
upper = np.array([90, 255, 255])

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # converte para hsv
    mask = cv2.inRange(image, lower, upper)
    imgStack = cvzone.stackImages([img, mask], 2, 1)

    contornos, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contornos) != 0:
        for contorno in contornos:
            if cv2.contourArea(contorno) > 100:
                # print(cv2.contourArea(contorno))
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(imgStack, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cx = x + w // 2
                cy = y + h // 2
                cv2.circle(imgStack, (cx, cy), 2, (0, 0, 255), -1)

    cv2.imshow("Image", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


import cv2  # Importa o módulo OpenCV para processamento de imagens
import numpy as np  # Importa o módulo NumPy para manipulação de arrays
from djitellopy import Tello  # Importa a biblioteca DJITelloPy para controlar o drone Tello
import time  # Importa o módulo time para manipulação de tempo
from FaceModule import FaceModule


"""
-------------------- DESCRIÇÃO --------------------
| TrackFace é uma classe que controla um drone    |
| durante a detecção e rastreamento de rostos,    |
| aproveitando funcionalidades de uma classe de   |
| detecção de rostos. Seu objetivo é permitir que |
| o drone siga ou mantenha distância de um rosto  |
| detectado, ajustando sua posição conforme o     |
| necessário                                      |
---------------------------------------------------
"""


class TrackFace(FaceModule):
    def __init__(self, size=(360, 240), pid=[0.4, 0.4, 0], fbRange=[6200, 6800]):
        super().__init__(size)
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()
        self.tello.takeoff()
        self.tello.send_rc_control(0, 0, 10, 0)
        self.pid = pid
        self.pError = 0
        self.fbRange = fbRange
        time.sleep(1)

    # Método para rastrear o rosto e controlar o movimento do drone
    def trackFace(self, info, pError):
        x, y = info[0]  # Extrai as coordenadas x e y do ponto central do rosto
        area = info[1]  # Extrai a área do retângulo ao redor do rosto

        error = x - self.w // 2
        speed = self.pid[0] * error + self.pid[1] * (error - pError)
        speed = int(np.clip(speed, -100, 100))  # Limita a velocidade para garantir que esteja dentro do intervalo permitido
        fb = 0

        # Verifica se a área do rosto está dentro da faixa desejada
        if self.fbRange[0] < area < self.fbRange[1]:
            fb = 0
        if area > self.fbRange[1]:
            fb = -20
        elif area < self.fbRange[0] and area != 0:
            fb = 20

        # Se a coordenada x do rosto for 0, ajusta a velocidade e o erro para 0 para evitar movimentos inesperados
        if x == 0:
            speed = 0
            error = 0

        self.tello.send_rc_control(0, fb, 0, speed)
        return error  # Retorna o erro para ser utilizado na próxima iteração


drone = TrackFace()
while True:
    print(drone.tello.get_battery())
    img = drone.tello.get_frame_read().frame  # Captura um frame do vídeo do drone
    img = cv2.resize(img, (drone.w, drone.h))  # Redimensiona o frame para as dimensões desejadas
    img, info = drone.findFace(img)  # Detecta e marca rostos no frame e retorna informações sobre o rosto dominante
    pError = drone.trackFace(info, drone.pError)  # Rastreia o rosto e controla o movimento do drone
    cv2.imshow("Saida", img)  # Mostra o frame processado com os rostos detectados
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Verifica se a tecla 'q' foi pressionada
        drone.tello.land()  # Aterra o drone
        break  # Sai do loop

cv2.destroyAllWindows()  # Fecha todas as janelas OpenCV

"""
w, h = 360, 240
fbRange = [6200, 6800]
udRange = [15, 15]
pid = [0.4, 0.4, 0]
pError = 0

tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()
tello.send_rc_control(0, 0, 15, 0)
time.sleep(2)


def conector(ssid, pswd):
    tello.connect_to_wifi(ssid, pswd)
    return tello


def findFace(img):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    faceList = []
    faceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        faceList.append([cx, cy])
        faceListArea.append(area)
    if len(faceListArea) != 0:
        i = faceListArea.index(max(faceListArea))
        return img, [faceList[i], faceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError, tello):
    x, y = info[0]
    area = info[1]
    error = x - w // 2
    error_y = y - h // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))
    fb = 0
    # ud = 15

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0
    print(error, fb)
    tello.send_rc_control(0, fb, 0, speed)
    return error


#######    tentativa de ajusta de altura #######
     if udRange[0] < area < udRange[1]:
        ud = 0
    elif area > udRange[1]:
        ud = -5
    elif area < udRange[0] and area != 0:
        ud = 5


# tello = conector('AP 102', '77981064271')
while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError, tello)
    cv2.imshow("Saida", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break

cv2.destroyAllWindows()
"""
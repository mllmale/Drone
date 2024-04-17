import cv2
from HandTrackModule import HandDetector
from djitellopy import Tello
import time

"""
------------------------ Descrição -------------------------
| Este código tem com intuito de usar a mão para fazer com |
| que o drone faça alguns comandos, sendo eles flipar,voar |
| pousar. Na última atualização feita, foi feito com que o |
| drone flip para a esquerda.                              |
------------------------------------------------------------
"""


class droneControl(HandDetector):
    def __init__(self):
        super().__init__(maxHands=1)
        self.tello = Tello()
        self.tello.connect()
        self.tello.takeoff()
        time.sleep(1)
        self.lmList = []

    def fingerDown(self, lmList, fingerS, fingerE, color=(0, 255, 0), thickness=2):
        if lmList[fingerS][2] > lmList[fingerE][2]:
            """start_point = (int(lmList[fingerS][1]), int(lmList[fingerS][2]))
            end_point = (int(lmList[fingerE][1]), int(lmList[fingerE][2]))
            cv2.line(img, start_point, end_point, color, thickness)"""
            return True
        else:
            return False

    def thumbDown(self, lmList):
        if lmList[4][1] < lmList[1][1]:
            """start_point = (int(lmList[fingerS][1]), int(lmList[fingerS][2]))
            end_point = (int(lmList[fingerE][1]), int(lmList[fingerE][2]))
            cv2.line(img, start_point, end_point, color, thickness)"""
            # print('passou')
            return True
        else:
            return False

    def findCommand(self, img):
        self.lmList = self.findPosition(img)
        if len(self.lmList) != 0:
            """
            thumb = lmList[4]
            pinky = lmList[20]
            iFinger = lmList[8]
            distance2 = ((iFinger[1] - thumb[1]) ** 2 + (iFinger[2] - thumb[2]) ** 2) ** 0.5
            distance = ((thumb[1] - pinky[1]) ** 2 + (thumb[2] - pinky[2]) ** 2) ** 0.5
            print(distance2)
            """
            command_conditions = {
                1: lambda lmList: self.fingerDown(lmList, 7, 5) and self.fingerDown(lmList, 11, 9) and not (
                    self.fingerDown(lmList, 19, 17)) and not self.thumbDown(lmList) and self.fingerDown(lmList, 15, 13),
                2: lambda lmList: self.fingerDown(lmList, 19, 17) and self.fingerDown(lmList, 11,
                                                                                      9) and not self.thumbDown(
                    lmList) and not (self.fingerDown(lmList, 7, 5)) and self.fingerDown(lmList, 15, 13),
                3: lambda lmList: self.fingerDown(lmList, 19, 17) and self.fingerDown(lmList, 15,
                                                                                      13) and self.fingerDown(lmList,
                                                                                                              11, ) and not self.fingerDown(
                    lmList, 7, 5) and self.thumbDown(lmList),
            }

            for command, condition_func in command_conditions.items():
                if condition_func(self.lmList):
                    print(command)
                    return command
        return 0

    def doCommand(self, command):
        command_functions = {
            1: self.tello.flip_left,
            2: self.tello.land,
            3: lambda: self.tello.move_forward(20),
        }
        if command in command_functions:
            command_functions[command]()
            time.sleep(1)


cap = cv2.VideoCapture(0)
drone = droneControl()

while True:
    _, img = cap.read()
    img = drone.findHand(img)
    command = drone.findCommand(img)

    drone.doCommand(command)
    print(drone.tello.get_battery())

    cv2.imshow("Imagem", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# tello.land()
cap.release()
cv2.destroyAllWindows()

"""
# Importando as bibliotecas necessárias
import cv2  # OpenCV para processamento de vídeo e imagens
from HandTrackModule import HandDetector  # Módulo personalizado para detecção de mãos
from djitellopy import Tello  # Biblioteca para controlar o drone Tello
import time  # Biblioteca para lidar com o tempo

# Conectando-se ao drone Tello e iniciando a transmissão de vídeo
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()  # Fazendo o drone decolar
time.sleep(2)  # Aguardando 2 segundos para estabilizar

# Inicializando o detector de mãos
detector = HandDetector(maxHands=1)

# Função para verificar se um dedo está dobrado
def fingerDown(lmList, fingerS, fingerE):
    # Verificando se a coordenada Y da landmark do dedo inicial é maior que a do dedo final
    if lmList[fingerS][2] > lmList[fingerE][2]:
        return True  # Retorna True se o dedo estiver dobrado
    else:
        return False  # Retorna False se o dedo não estiver dobrado

# Função para identificar o comando com base na posição da mão
def findCommand(img):
    lmList = detector.findPosition(img)  # Obtendo a posição das landmarks das mãos
    if len(lmList) != 0:
        thumb = lmList[4]  # Posição do polegar
        pinky = lmList[20]  # Posição do mindinho
        cv2.line(img, (thumb[1], thumb[2]), (pinky[1], pinky[2]), (0, 255, 0), 2)  # Desenhando uma linha entre o polegar e o mindinho
        distance = ((thumb[1] - pinky[1]) ** 2 + (thumb[2] - pinky[2]) ** 2) ** 0.5  # Calculando a distância entre o polegar e o mindinho
        # Verificando se todos os dedos estão dobrados e a distância entre o polegar e o mindinho está dentro de uma faixa específica
        if fingerDown(lmList, 8, 7) and fingerDown(lmList, 12, 11) and fingerDown(lmList, 16, 15) and (250 > distance > 200):
            return 1  # Comando para realizar um flip
        else:
            return -1  # Nenhum comando identificado

# Função para realizar um flip com o drone Tello
def flipDrone(tello, command):
    if command == 1:
        tello.flip_left()  # Realizando um flip para a esquerda

# Inicializando a captura de vídeo da webcam
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()  # Capturando um frame da webcam
    img = detector.findHand(img)  # Detectando mãos na imagem
    command = findCommand(img)  # Identificando o comando com base na posição da mão
    flipDrone(tello, command)  # Realizando a ação correspondente ao comando identificado
    cv2.imshow("Imagem", img)  # Exibindo a imagem com as mãos detectadas

    # Verificando se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.land()  # Fazendo o drone pousar
cap.release()  # Liberando o dispositivo de captura de vídeo
cv2.destroyAllWindows()  # Fechando todas as janelas de exibição

"""

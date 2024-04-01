import cv2
import mediapipe as mp

"""
------------------------ Descrição -------------------------
| Este módulo leva consigo uma classes para detecção e     |
| localização de uma mão, para, posteriormente, ser usada  |
| em outros projetos.                                       |
------------------------------------------------------------
"""


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0, trackCon=0.5):
        self.res = None
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw=True):
        img = cv2.flip(img, 2)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(imgRGB)
        if self.res.multi_hand_landmarks:
            for handLms in self.res.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.res is not None and self.res.multi_hand_landmarks:
            myHand = self.res.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                # print(id, cx, cy)

                if draw: pass
                # cv2.circle(img, (cx, cy), 1, (255, 255, 0), cv2.FILLED)

        return lmList


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        _, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            pass
            # print(lmList[4])

        cv2.imshow("Imagem", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()


"""
# Importando as bibliotecas necessárias
import cv2  # OpenCV para processamento de vídeo e imagens
import mediapipe as mp  # MediaPipe para detecção de mãos

# Definindo uma classe para detectar mãos
class HandDetector():
    # Método de inicialização da classe
    def __init__(self, mode=False, maxHands=2, detectionCon=0, trackCon=0.5):
        # Inicializando variáveis de configuração
        self.res = None  # Variável para armazenar o resultado da detecção de mãos
        self.mode = mode  # Modo de detecção de mãos (padrão é False)
        self.maxHands = maxHands  # Número máximo de mãos a serem detectadas (padrão é 2)
        self.detectionCon = detectionCon  # Confiança mínima para detecção (padrão é 0)
        self.trackCon = trackCon  # Confiança mínima para rastreamento (padrão é 0.5)
        # Inicializando o modelo de detecção de mãos do MediaPipe
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        # Inicializando o módulo de desenho do MediaPipe
        self.mpDraw = mp.solutions.drawing_utils

    # Método para encontrar as mãos na imagem
    def findHand(self, img, draw=True):
        # Espelhando a imagem horizontalmente
        img = cv2.flip(img, 2)
        # Convertendo a imagem para o formato RGB (MediaPipe utiliza RGB)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Processando a detecção de mãos na imagem
        self.res = self.hands.process(imgRGB)
        # Verificando se foram detectadas múltiplas mãos
        if self.res.multi_hand_landmarks:
            # Desenhando as conexões das mãos na imagem
            for handLms in self.res.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)
        return img

    # Método para encontrar a posição das landmarks das mãos na imagem
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []  # Lista para armazenar as landmarks das mãos

        # Verificando se há resultados de detecção de mãos e se existem múltiplas mãos
        if self.res is not None and self.res.multi_hand_landmarks:
            # Obtendo a mão desejada
            myHand = self.res.multi_hand_landmarks[handNo]

            # Iterando sobre as landmarks da mão
            for id, lm in enumerate(myHand.landmark):
                # Obtendo as dimensões da imagem
                h, w, c = img.shape
                # Obtendo as coordenadas normalizadas das landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])  # Armazenando as coordenadas das landmarks na lista
        return lmList

# Função principal do programa
def main():
    cap = cv2.VideoCapture(0)  # Inicializando a captura de vídeo da webcam
    detector = HandDetector()  # Inicializando o detector de mãos
    while True:
        _, img = cap.read()  # Capturando um frame da webcam
        img = detector.findHand(img)  # Detectando mãos na imagem
        lmList = detector.findPosition(img)  # Obtendo a posição das landmarks das mãos
        cv2.imshow("Imagem", img)  # Exibindo a imagem com as mãos detectadas

        # Verificando se a tecla 'q' foi pressionada para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Executando a função principal se este script for o principal
if __name__ == '__main__':
    main()

"""

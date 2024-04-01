
import cv2  # Importa o módulo OpenCV para processamento de imagens
import numpy as np  # Importa o módulo NumPy para manipulação de arrays
from djitellopy import Tello  # Importa a biblioteca DJITelloPy para controlar o drone Tello
import time  # Importa o módulo time para manipulação de tempo

# Definição das dimensões da imagem de entrada (largura e altura)
w, h = 360, 240

# Faixa de área do rosto para determinar se o rosto está próximo ou distante
fbRange = [6200, 6800]

# Faixa de desvio vertical permitido para ajustar a altitude do drone
udRange = [15, 15]

# Coeficientes PID para controle proporcional do erro
pid = [0.4, 0.4, 0]

# Variável para armazenar o erro anterior para o controle PID
pError = 0

# Inicializa o objeto Tello para comunicação com o drone
tello = Tello()
tello.connect()  # Conecta-se ao drone Tello
tello.streamon()  # Inicia a transmissão de vídeo do drone
tello.takeoff()  # Inicia o voo do drone
tello.send_rc_control(0, 0, 15, 0)  # Envia comandos de controle para manter o drone estável
time.sleep(2)  # Aguarda 2 segundos para garantir a estabilidade do drone


# Função para conectar o drone a uma rede Wi-Fi específica
def conector(ssid, pswd):
    tello.connect_to_wifi(ssid, pswd)  # Conecta o drone à rede Wi-Fi especificada
    return tello  # Retorna o objeto Tello


# Função para detectar rostos na imagem de entrada
def findFace(img):
    # Carrega o classificador em cascata para detecção de rostos
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Converte a imagem de entrada em tons de cinza
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta rostos na imagem em tons de cinza
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    faceList = []  # Lista para armazenar as coordenadas dos centros dos rostos
    faceListArea = []  # Lista para armazenar as áreas dos rostos detectados

    # Itera sobre os rostos detectados
    for (x, y, w, h) in faces:
        # Desenha um retângulo em volta do rosto detectado
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Calcula as coordenadas do centro do rosto
        cx = x + w // 2
        cy = y + h // 2

        # Calcula a área do rosto
        area = w * h

        # Desenha um círculo no centro do rosto
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        # Adiciona as coordenadas do centro do rosto e sua área às listas
        faceList.append([cx, cy])
        faceListArea.append(area)

    # Verifica se foram detectados rostos na imagem
    if len(faceListArea) != 0:
        # Identifica o índice do maior rosto na lista
        i = faceListArea.index(max(faceListArea))

        # Retorna a imagem com o rosto marcado e as coordenadas do rosto dominante
        return img, [faceList[i], faceListArea[i]]
    else:
        # Retorna a imagem sem alterações e coordenadas vazias
        return img, [[0, 0], 0]


# Função para rastrear o rosto e controlar o movimento do drone
def trackFace(info, w, pid, pError, tello):
    # Extrai as coordenadas x e y do ponto central do rosto e a área do retângulo ao redor do rosto
    x, y = info[0]
    area = info[1]

    # Calcula o erro de posicionamento do rosto em relação ao centro da tela
    error = x - w // 2

    # Calcula a velocidade com base no erro atual e no erro anterior
    speed = pid[0] * error + pid[1] * (error - pError)

    # Limita a velocidade para garantir que esteja dentro do intervalo permitido
    speed = int(np.clip(speed, -100, 100))

    # Inicializa a velocidade de avanço/recuo (forward/backward) como 0
    fb = 0

    # Verifica se o rosto está dentro do intervalo desejado em relação à área
    if fbRange[0] < area < fbRange[1]:
        fb = 0
    # Se a área do rosto for maior do que o intervalo desejado, move o drone para trás
    if area > fbRange[1]:
        fb = -20
    # Se a área do rosto for menor do que o intervalo desejado e diferente de 0, move o drone para frente
    elif area < fbRange[0] and area != 0:
        fb = 20

    # Se a coordenada x do rosto for 0, ajusta a velocidade e o erro para 0 para evitar movimentos inesperados
    if x == 0:
        speed = 0
        error = 0

    # Envia os comandos de controle de movimento para o drone
    tello.send_rc_control(0, fb, 0, speed)

    # Retorna o erro para ser utilizado na próxima iteração
    return error


"""
    tentativa de ajusta de altura
     if udRange[0] < area < udRange[1]:
        ud = 0
    elif area > udRange[1]:
        ud = -5
    elif area < udRange[0] and area != 0:
        ud = 5

"""

# tello = conector('AP 102', '77981064271')
while True:
    print(tello.get_battery())
    img = tello.get_frame_read().frame  # Captura um frame do vídeo do drone
    img = cv2.resize(img, (w, h))  # Redimensiona o frame para as dimensões desejadas
    img, info = findFace(img)  # Detecta e marca rostos no frame e retorna informações sobre o rosto dominante
    pError = trackFace(info, w, pid, pError, tello)  # Rastreia o rosto e controla o movimento do drone
    cv2.imshow("Saida", img)  # Mostra o frame processado com os rostos detectados
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Verifica se a tecla 'q' foi pressionada
        tello.land()  # Aterra o drone
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
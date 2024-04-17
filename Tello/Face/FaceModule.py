import cv2

"""
----------------------- DESCRIÇÃO -------------------------
| Esta classe é responsável por detectar rostos em uma    |
| imagem fornecida. Utiliza o classificador em cascata    |
| Haar para realizar a detecção de rostos em tons de cinza|
| da imagem de entrada. Após a detecção, marca os rostos  |
| encontrados com retângulos vermelhos e identifica o     |
| centro de cada rosto com um círculo verde. A área de    |
| cada rosto detectado é calculada e as coordenadas do    |
| centro do rosto, juntamente com sua área, são retornadas|
| como informações sobre o rosto dominante na imagem. Caso|
| nenhum rosto seja detectado, retorna coordenadas vazias.|
----------------------------------------------------------- 
 
"""


class FaceModule:
    def __init__(self, size=(360, 240)):
        self.w, self.h = size

    def findFace(self, img):
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

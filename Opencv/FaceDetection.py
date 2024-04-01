import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2

cap = cv2.VideoCapture(0)

# Inicializa um objeto de FaceDetector
# minDetectorCon: limiar de mínima confiabilidade, ou seja, se ele tiver 50% de ctz
#                 ele irá detectar o rosto
# modelSelection: 0 para curta distância, 1 para longa
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

while True:
    _, img = cap.read()

    # bbox = Lista de bounding box em volta do rosto detectado (retangulo)
    img, bboxs = detector.findFaces(img)

    # checa se alguma face foi detectada
    if bboxs:
        for bbox in bboxs:
            # bbox possui 'id', 'bbox', 'score' , 'centro'
            # Get data
            center = bbox['center']
            x, y, w, h = bbox['bbox']
            score = int(bbox['score'][0] * 100)

            # desenha
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            # cvzone.putTextRect(img, f'{score}%', {x, y - 10})
            cvzone.cornerRect(img, (x, y, w, h))

            cv2.imshow("Detecção de rosto", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

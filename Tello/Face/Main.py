import cv2
from FaceTracking import TrackFace

"""
---------------- DESCRIÇÃO ----------------
| Este script controla um drone Tello para|
| detectar e rastrear rostos em tempo real|
| utilizando a classe `TrackFace`.        |
| Ele decola, ajusta o voo para manter o  |
| rosto dentro de uma faixa específica na |
| imagem e pousa quando a tecla 'q' é     |
|pressionada.                             |
-------------------------------------------

"""


def main():
    drone = TrackFace()
    while True:
        print(drone.tello.get_battery())
        img = drone.tello.get_frame_read().frame  # Captura um frame do vídeo do drone
        img = cv2.resize(img, (drone.w, drone.h))  # Redimensiona o frame para as dimensões desejadas
        img, info = drone.findFace(img)  # Detecta e marca rostos no frame e retorna informações sobre o rosto dominante
        pError = drone.trackFace(info, pError)  # Rastreia o rosto e controla o movimento do drone
        cv2.imshow("Saida", img)  # Mostra o frame processado com os rostos detectados
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Verifica se a tecla 'q' foi pressionada
            drone.tello.land()  # Aterra o drone
            break  # Sai do loop

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

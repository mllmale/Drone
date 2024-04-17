from Tello.Hand.HandTracking import droneControl
import cv2


def main():
    drone = droneControl()
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        img = drone.findHand(img)
        command = drone.findCommand(img)

        drone.doCommand(command)
        print(drone.tello.get_battery())

        cv2.imshow("Imagem", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

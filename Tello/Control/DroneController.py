from MapControl import VideoControl
from djitellopy import Tello
import time
import pygame as pg


class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        # self.tello.streamon()
        self.control = VideoControl()
        time.sleep(2)

    def set_moviment(self):
        lr, fb, up, yv = 0, 0, 0, 0
        speed = 50
        for event in self.control.events:
            if event.type == pg.JOYAXISMOTION:
                velocity = int(speed + event.value * speed - 1)
                # Verifique o eixo X (esquerda/direita)
                if event.axis == 2:
                    if 0 < event.value <= 1:
                        lr = velocity
                    elif -1 <= event.value < 0:
                        lr = velocity

                # Verifique o eixo Y (frente/trás)
                elif event.axis == 3:
                    if 0 < event.value <= 1:
                        up = velocity
                    elif -1 <= event.value < 0:
                        print(event.value)
                        up = velocity

                # Verifique o eixo de rotação (yaw)
                elif event.axis == 0:
                    if 0 < event.value <= 1:
                        yv = velocity
                    elif -1 <= event.value < 0:
                        yv = velocity

                # Verifique o eixo de inclinação (pitch)
                elif event.axis == 1:
                    if 0 < event.value <= 1:
                        fb = int(speed + event.value * speed - 1)
                    elif -1 <= event.value < 0:
                        fb = int(speed + event.value * speed - 1)
                        print(event.value)

            # Verifique o estado dos botões de direção
        direction = self.control.get_dir()
        if direction == (0, 1):
            self.tello.takeoff()
        elif direction == (0, -1):
            self.tello.land()

        return lr, fb, up, yv


def main():
    drone = DroneController()

    while True:
        vals = drone.set_moviment()
        print(list(vals))
        drone.tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        drone.control.events = pg.event.get()
        # Captura a imagem do dron

        # Mostra o nível da bateria
        print("Nível da bateria:", drone.tello.get_battery())

    drone.tello.land()
    drone.tello.end()


if __name__ == "__main__":
    main()

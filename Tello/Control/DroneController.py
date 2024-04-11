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
                match event.axis:
                    case 0:
                        # Verifique o eixo de rotação (yaw)
                        # gira
                        if 0 < event.value <= 1:
                            yv = int(speed + event.value * speed - 1)
                        elif -1 <= event.value < 0:
                            yv = int(-speed + event.value * speed + 1)
                    case 1:
                        # Verifique o eixo de inclinação (pitch)
                        # vai para frente ou tras
                        if 0 < event.value <= 1:
                            fb = int(-speed + event.value * speed + 1)
                        elif -1 <= event.value < 0:
                            fb = int(speed + event.value * speed - 1)
                    case 2:
                        # Verifique o eixo X (esquerda/direita)
                        if 0 < event.value <= 1:
                            lr = int(speed + event.value * speed - 1)
                        elif -1 <= event.value < 0:
                            lr = int(-speed + event.value * speed + 1)
                    case 3:
                        # Verifique o eixo Y (frente/trás)
                        # sobe e desce
                        if 0 < event.value <= 1:
                            up = int(-speed + event.value * speed + 1)
                        elif -1 <= event.value < 0:
                            print(event.value)
                            up = int(speed + event.value * speed + 1)
                    case _:
                        pass
        return lr, fb, up, yv

    def fly(self):
        direction = self.control.get_dir()
        if direction is not None:
            print(direction)
            match direction:
                case (0, 1):
                    self.tello.takeoff()
                case (0, -1):
                    self.tello.land()
                case _:
                    pass

    def flip(self):
        button = self.control.get_button()
        if button is not None:
            print(button)
            match button:
                case 0:
                    self.tello.flip_forward()
                case 1:
                    self.tello.flip_right()
                case 2:
                    self.tello.flip_left()
                case 3:
                    self.tello.flip_back()
                case _:
                    pass

def main():
    drone = DroneController()

    while True:
        vals = drone.set_moviment()
        print(list(vals))
        drone.tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        drone.control.events = pg.event.get()
        drone.fly()
        drone.flip()
        # Captura a imagem do dron

        # Mostra o nível da bateria
        print("Nível da bateria:", drone.tello.get_battery())

    drone.tello.land()
    drone.tello.end()


if __name__ == "__main__":
    main()

from DroneController import DroneController
import pygame as pg


def main():

    drone = DroneController()

    while True:
        vals = drone.set_moviment()
        print(list(vals))
        drone.tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        drone.control.events = pg.event.get()
        drone.fly()
        drone.flip()


if __name__ == '__main__':
    main()

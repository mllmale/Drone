from DroneController import DroneController
from MapControl import VideoControl
import pygame as pg
import time


def main():

    control = VideoControl()
    drone = DroneController()

    control.map_buttons()

    while True:
        vals = drone.set_moviment()
        drone.tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        drone.control.events = pg.event.get()


if __name__ == '__main__':
    main()

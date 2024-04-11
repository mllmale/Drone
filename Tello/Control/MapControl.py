import pygame as pg
import sys

"""
Comandos
0 -> y
1 -> b
2 -> a
3 -> x
4 -> LB
5 -> RB
6 -> LT
7 -> RT
8 -> select
9 -> start
10 -> LS
11 -> RS

"""


class VideoControl:
    def __init__(self):
        pg.init()
        pg.joystick.init()
        if pg.joystick.get_count() == 0:
            print("Nenhum joystick detectado.")
            pg.quit()
            sys.exit()
        self.joystick = pg.joystick.Joystick(0)
        self.joystick.init()
        # Mapeamento de botões
        self.button_map = {}
        self.events = []
        self.axis_positions = {i: 0 for i in range(pg.joystick.get_count())}

    def map_buttons(self):
        for i in range(self.joystick.get_numbuttons()):
            self.button_map[i] = i

    def get_button(self):
        for event in self.events:
            if event.type == pg.JOYBUTTONDOWN:
                return event.button
        return None

    def get_axis_position(self, axis):
        for event in self.events:
            if event.type == pg.JOYAXISMOTION:
                if event.axis == axis:
                    self.axis_positions[axis] = event.value
                    return event.value
        if axis in self.axis_positions:
            return self.axis_positions[axis]
        else:
            return 0

    def update_events(self):
        self.events = pg.event.get()

    def get_dir(self):
        for event in self.events:
            if event.type == pg.JOYHATMOTION:
                return event.value
        return None


# Loop principal
if __name__ == "__main__":
    control = VideoControl()
    control.map_buttons()
    while True:
        control.events = pg.event.get()
        button_pressed = control.get_button()
        # print(type(button_pressed))
        axis = control.get_axis_position(3)
        hat = control.get_dir()
        if button_pressed is not None:
           print(button_pressed)


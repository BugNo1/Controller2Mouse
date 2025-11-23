import time
import pygame
from pynput import mouse, keyboard

JOYSTICK_1 = 0
JOYSTICK_2 = 1
Y_OFFSET_MAX = 90
X_OFFSET_MAX = 90

class EventHandler:
    def __init__(self):
        self._x_offset = 0
        self._y_offset = 0
        self._mouse = mouse.Controller()
        self._keyboard = keyboard.Controller()

    def run(self):
        done = False
        while not done:
            # Event processing
            # PyGame seems to have an issue with event processing - But when Steam is running everything is fine!
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.JOYBUTTONDOWN:
                    self._handle_button_down_event(event)

                if event.type == pygame.JOYBUTTONUP:
                    self._handle_button_up_event(event)

                if event.type == pygame.JOYAXISMOTION:
                    self._handle_axis_motion_event(event)

            self._mouse.move(int(self._x_offset), int(self._y_offset))
            time.sleep(0.05)  # needed to not overload the event system

    def _handle_button_down_event(self, event):
        # print(event.button)
        if event.instance_id == JOYSTICK_1:
            self._handle_button_down_event_joystick_1(event)
        elif event.instance_id == JOYSTICK_2:
            self._handle_button_down_event_joystick_2(event)

    def _handle_button_down_event_joystick_1(self, event):
        if event.button == 0:  # cross button
            self._mouse.press(mouse.Button.left)
        if event.button == 1:  # circle button
            self._keyboard.press(keyboard.Key.esc)
        if event.button == 2:  # square button
            self._keyboard.press(keyboard.Key.space)
        if event.button == 3:  # triangle button
            self._mouse.press(mouse.Button.right)
        if event.button == 6:  # options button
            self._keyboard.press(keyboard.Key.f5)
        if event.button == 11:  # up button
            self._keyboard.press(keyboard.Key.up)
        if event.button == 12:  # down button
            self._keyboard.press(keyboard.Key.down)
        if event.button == 13:  # left button
            self._keyboard.press(keyboard.Key.left)
        if event.button == 14:  # right button
            self._keyboard.press(keyboard.Key.right)

    def _handle_button_down_event_joystick_2(self, event):
        pass

    def _handle_button_up_event(self, event):
        if event.instance_id == JOYSTICK_1:
            self._handle_button_up_event_joystick_1(event)
        elif event.instance_id == JOYSTICK_2:
            self._handle_button_up_event_joystick_2(event)

    def _handle_button_up_event_joystick_1(self, event):
        if event.button == 0:  # cross button
            self._mouse.release(mouse.Button.left)
        if event.button == 1:  # circle button
            self._keyboard.release(keyboard.Key.esc)
        if event.button == 2:  # square button
            self._keyboard.release(keyboard.Key.space)
        if event.button == 3:  # triangle button
            self._mouse.release(mouse.Button.right)
        if event.button == 6:  # options button
            self._keyboard.release(keyboard.Key.f5)
        if event.button == 11:  # up button
            self._keyboard.release(keyboard.Key.up)
        if event.button == 12:  # down button
            self._keyboard.release(keyboard.Key.down)
        if event.button == 13:  # left button
            self._keyboard.release(keyboard.Key.left)
        if event.button == 14:  # right button
            self._keyboard.release(keyboard.Key.right)

    def _handle_button_up_event_joystick_2(self, event):
        pass

    def _handle_axis_motion_event(self, event):
        if event.instance_id == JOYSTICK_1:
            self._handle_axis_motion_event_joystick_1(event)
        elif event.instance_id == JOYSTICK_2:
            self._handle_axis_motion_event_joystick_2(event)

    def _handle_axis_motion_event_joystick_1(self, event):
        joystick = joysticks[event.instance_id]
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        if y <= -0.1:
            # print("up: %0.2f" % y)
            self._y_offset = y * Y_OFFSET_MAX
        if y >= 0.1:
            # print("down: %0.2f" % y)
            self._y_offset = y * Y_OFFSET_MAX
        if (y > -0.1) and (y < 0.1):
            # print("y centered: %0.2f" % y)
            self._y_offset = 0
        if x <= -0.1:
            # print("left: %0.2f" % x)
            self._x_offset = x * X_OFFSET_MAX
        if x >= 0.1:
            # print("right: %0.2f" % x)
            self._x_offset = x * X_OFFSET_MAX
        if (x > -0.1) and (x < 0.1):
            # print("x centered: %0.2f" % x)
            self._x_offset = 0

    def _handle_axis_motion_event_joystick_2(self, event):
        pass

# TODO:
 # right joystick = arrow keys (repeat)
 # second joystick: arrow keys, cross, triangle, circle, square

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("Number of Joysticks found: %d" % len(joysticks))

    event_handler = EventHandler()
    event_handler.run()

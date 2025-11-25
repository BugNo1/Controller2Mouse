import time
import pygame
from enum import Enum
from pynput import mouse, keyboard
from key_repeater import KeyRepeater

JOYSTICK_1 = 0
JOYSTICK_2 = 1
Y_OFFSET_MAX = 90
X_OFFSET_MAX = 90

class Direction(Enum):
    UP          = 0
    DOWN        = 1
    UD_CENTERED = 2
    LEFT        = 3
    RIGHT       = 4
    LR_CENTERED = 5

class EventHandler:
    def __init__(self):
        self._x_offset = 0
        self._y_offset = 0
        self._mouse = mouse.Controller()
        self._keyboard = keyboard.Controller()
        self._thread_pool_joystick_1 = dict()

    def run(self):
        self._add_repeater(Direction.UP, "Joystick 1 UP", self._thread_pool_joystick_1,
                           self._keyboard.press, self._keyboard.release, keyboard.Key.up)
        self._add_repeater(Direction.DOWN, "Joystick 1 DOWN", self._thread_pool_joystick_1,
                           self._keyboard.press, self._keyboard.release, keyboard.Key.down)
        self._add_repeater(Direction.LEFT, "Joystick 1 LEFT", self._thread_pool_joystick_1,
                           self._keyboard.press, self._keyboard.release, keyboard.Key.left)
        self._add_repeater(Direction.RIGHT, "Joystick 1 RIGHT", self._thread_pool_joystick_1,
                           self._keyboard.press, self._keyboard.release, keyboard.Key.right)

        try:
            done = False
            while not done:
                # Event processing
                # On macOS: PyGame seems to have an issue with event processing (events are not fired) - But when Steam is running everything is fine!
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
        except KeyboardInterrupt:
            for repeater in self._thread_pool_joystick_1.values():
                repeater.stop()
                repeater.join()

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
        self._handle_axis_motion_event_joystick_1_left_stick(joystick)
        self._handle_axis_motion_event_joystick_1_right_stick(joystick)

    def _handle_axis_motion_event_joystick_1_left_stick(self, joystick):
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        x, y, _, _ = self._filter_axis(x, y)
        self._y_offset = y * Y_OFFSET_MAX
        self._x_offset = x * X_OFFSET_MAX

    def _handle_axis_motion_event_joystick_1_right_stick(self, joystick):
        x = joystick.get_axis(2)
        y = joystick.get_axis(3)
        x, y, x_direction, y_direction = self._filter_axis(x, y)

        if x_direction == Direction.LR_CENTERED:
            self._thread_pool_joystick_1[Direction.LEFT].set_delay(x)
            self._thread_pool_joystick_1[Direction.RIGHT].set_delay(x)
        else:
            self._thread_pool_joystick_1[x_direction].set_delay(x)

        if y_direction == Direction.UD_CENTERED:
            self._thread_pool_joystick_1[Direction.UP].set_delay(y)
            self._thread_pool_joystick_1[Direction.DOWN].set_delay(y)
        else:
            self._thread_pool_joystick_1[y_direction].set_delay(y)

    def _handle_axis_motion_event_joystick_2(self, event):
        pass

    def _filter_axis(self, x, y):
        filtered_x = 0
        filtered_y = 0
        direction_x = Direction.LR_CENTERED
        direction_y = Direction.UD_CENTERED

        if y <= -0.1:
            # print("up: %0.2f" % y)
            filtered_y = y
            direction_y = Direction.UP
        if y >= 0.1:
            # print("down: %0.2f" % y)
            filtered_y = y
            direction_y = Direction.DOWN
        if (y > -0.1) and (y < 0.1):
            # print("y centered: %0.2f" % y)
            filtered_y = 0
            direction_y = Direction.UD_CENTERED
        if x <= -0.1:
            # print("left: %0.2f" % x)
            filtered_x = x
            direction_x = Direction.LEFT
        if x >= 0.1:
            # print("right: %0.2f" % x)
            filtered_x = x
            direction_x = Direction.RIGHT
        if (x > -0.1) and (x < 0.1):
            # print("x centered: %0.2f" % x)
            filtered_x = 0
            direction_x = Direction.LR_CENTERED
        return filtered_x, filtered_y, direction_x, direction_y

    def _add_repeater(self, direction, name, thread_pool, press_function, release_function, button):
        repeater = KeyRepeater(0.0, name, press_function, release_function, button)
        repeater.start()
        thread_pool[direction] = repeater

# TODO:
 # second joystick: arrow keys, cross, triangle, circle, square
 # introduce JoystickEventMapper class

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("Number of Joysticks found: %d" % len(joysticks))

    event_handler = EventHandler()
    event_handler.run()

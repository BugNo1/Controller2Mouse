import time
import pygame
from pynput import mouse, keyboard
from event_mapper import EventMapper
from event import ControllerEvent, ControllerEventType

JOYSTICK_1 = 0
JOYSTICK_2 = 1

MOUSE = mouse.Controller()
KEYBOARD = keyboard.Controller()

CONFIGURATION_JOYSTICK_1 = {
    "name": "Joystick 1",
    "left_stick_is_mouse": True,
    "events": {
        ControllerEvent.UP: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.up},
        ControllerEvent.DOWN: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.down},
        ControllerEvent.LEFT: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.left},
        ControllerEvent.RIGHT: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.right},
        ControllerEvent.CROSS: {"press": MOUSE.press, "release": MOUSE.release, "button": mouse.Button.left},
        ControllerEvent.SQUARE: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.space},
        ControllerEvent.TRIANGLE: {"press": MOUSE.press, "release": MOUSE.release, "button": mouse.Button.right},
        ControllerEvent.CIRCLE: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.space},
        ControllerEvent.OPTIONS: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.f5}
    }
}

CONFIGURATION_JOYSTICK_2 = {
    "name": "Joystick 2",
    "left_stick_is_mouse": False,
    "events": {
        ControllerEvent.UP: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.up},
        ControllerEvent.DOWN: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.down},
        ControllerEvent.LEFT: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.left},
        ControllerEvent.RIGHT: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.right},
        ControllerEvent.CROSS: {"press": MOUSE.press, "release": MOUSE.release, "button": mouse.Button.left},
        ControllerEvent.SQUARE: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.space},
        ControllerEvent.TRIANGLE: {"press": MOUSE.press, "release": MOUSE.release, "button": mouse.Button.right},
        ControllerEvent.CIRCLE: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.space},
        ControllerEvent.OPTIONS: {"press": KEYBOARD.press, "release": KEYBOARD.release, "button": keyboard.Key.f5}
    }
}

class EventHandler:
    def __init__(self, event_mapper_joystick_1, event_mapper_joystick_2):
        self._x_offset = 0
        self._y_offset = 0
        #self._mouse = mouse.Controller()
        #self._keyboard = keyboard.Controller()
        #self._thread_pool_joystick_1 = dict()
        self._event_mapper_joystick_1 = event_mapper_joystick_1
        self._event_mapper_joystick_2 = event_mapper_joystick_2

    def run(self):
        try:
            done = False
            while not done:
                # Event processing
                # On macOS: PyGame seems to have an issue with event processing (events are not fired).
                # But when Steam is running everything is fine ("PlayStation Controller Support" must be set to "Enabled")!
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

                    if event.type == pygame.JOYBUTTONDOWN:
                        self._handle_button_down_event(event)

                    if event.type == pygame.JOYBUTTONUP:
                        self._handle_button_up_event(event)

                    if event.type == pygame.JOYAXISMOTION:
                        self._handle_axis_motion_event(event)

                MOUSE.move(int(self._x_offset), int(self._y_offset))
                time.sleep(0.05)  # needed to not overload the event system
        except KeyboardInterrupt:
            self._event_mapper_joystick_1.stop()
            self._event_mapper_joystick_2.stop()

    def _handle_button_down_event(self, event):
        if event.instance_id == JOYSTICK_1:
            self._event_mapper_joystick_1.handle_button_event(event, ControllerEventType.PRESS)
        elif event.instance_id == JOYSTICK_2:
            self._event_mapper_joystick_2.handle_button_event(event, ControllerEventType.PRESS)

    def _handle_button_up_event(self, event):
        if event.instance_id == JOYSTICK_1:
            self._event_mapper_joystick_1.handle_button_event(event, ControllerEventType.RELEASE)
        elif event.instance_id == JOYSTICK_2:
            self._event_mapper_joystick_2.handle_button_event(event, ControllerEventType.RELEASE)

    def _handle_axis_motion_event(self, event):
        if event.instance_id == JOYSTICK_1:
            self._x_offset, self._y_offset = self._event_mapper_joystick_1.handle_axis_motion_event(joysticks[event.instance_id], self._x_offset, self._y_offset)
        elif event.instance_id == JOYSTICK_2:
            self._x_offset, self._y_offset = self._event_mapper_joystick_2.handle_axis_motion_event(joysticks[event.instance_id], self._x_offset, self._y_offset)
# TODO:
 # second joystick: arrow keys, cross, triangle, circle, square, right stick, (left stick disabled)
 # move event handler to separate file

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("Number of Joysticks found: %d" % len(joysticks))

    event_mapper_joystick_1 = EventMapper(CONFIGURATION_JOYSTICK_1)
    event_mapper_joystick_2 = EventMapper(CONFIGURATION_JOYSTICK_2)

    event_handler = EventHandler(event_mapper_joystick_1, event_mapper_joystick_2)
    event_handler.run()

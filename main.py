import pygame
from pynput import mouse, keyboard
from event_handler import EventHandler
from event_mapper import EventMapper
from event import ControllerEvent

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

# TODO:
 # second joystick: arrow keys, cross, triangle, circle, square, right stick, (left stick disabled)

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("Number of Joysticks found: %d" % len(joysticks))

    event_mapper_joystick_1 = EventMapper(CONFIGURATION_JOYSTICK_1)
    event_mapper_joystick_2 = EventMapper(CONFIGURATION_JOYSTICK_2)

    event_handler = EventHandler(joysticks, event_mapper_joystick_1, event_mapper_joystick_2, MOUSE)
    event_handler.run()

import time
import pygame
from event import ControllerEventType

JOYSTICK_1 = 0
JOYSTICK_2 = 1

class EventHandler:
    def __init__(self, joysticks, event_mapper_joystick_1, event_mapper_joystick_2, mouse):
        self._x_offset = 0
        self._y_offset = 0
        self._joysticks = joysticks
        self._event_mapper_joystick_1 = event_mapper_joystick_1
        self._event_mapper_joystick_2 = event_mapper_joystick_2
        self._mouse = mouse

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

                self._mouse.move(int(self._x_offset), int(self._y_offset))
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
            self._x_offset, self._y_offset = self._event_mapper_joystick_1.handle_axis_motion_event(self._joysticks[event.instance_id], self._x_offset, self._y_offset)
        elif event.instance_id == JOYSTICK_2:
            self._x_offset, self._y_offset = self._event_mapper_joystick_2.handle_axis_motion_event(self._joysticks[event.instance_id], self._x_offset, self._y_offset)

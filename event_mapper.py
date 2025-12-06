from event import ControllerEvent, ControllerEventType
from key_repeater import KeyRepeater

Y_OFFSET_MAX = 90
X_OFFSET_MAX = 90

class EventMapper:
    def __init__(self, configuration):
        self._name = configuration["name"]
        self._left_stick_is_mouse = configuration["left_stick_is_mouse"]
        self._events = configuration["events"]
        self._thread_pool = dict()
        self._add_repeater(ControllerEvent.UP, self._name + " UP")
        self._add_repeater(ControllerEvent.DOWN, self._name + " DOWN")
        self._add_repeater(ControllerEvent.LEFT, self._name + " LEFT")
        self._add_repeater(ControllerEvent.RIGHT, self._name + " RIGHT")

    def handle_button_event(self, event, event_type):
        # print(event.button)
        if event.button == 0:  # cross button
            self._execute_button_event(ControllerEvent.CROSS, event_type)
        if event.button == 1:  # circle button
            self._execute_button_event(ControllerEvent.CIRCLE, event_type)
        if event.button == 2:  # square button
            self._execute_button_event(ControllerEvent.SQUARE, event_type)
        if event.button == 3:  # triangle button
            self._execute_button_event(ControllerEvent.TRIANGLE, event_type)
        if event.button == 6:  # options button
            self._execute_button_event(ControllerEvent.OPTIONS, event_type)
        if event.button == 11:  # up button
            self._execute_button_event(ControllerEvent.UP, event_type)
        if event.button == 12:  # down button
            self._execute_button_event(ControllerEvent.DOWN, event_type)
        if event.button == 13:  # left button
            self._execute_button_event(ControllerEvent.LEFT, event_type)
        if event.button == 14:  # right button
            self._execute_button_event(ControllerEvent.RIGHT, event_type)

    def _execute_button_event(self, controller_event, controller_event_type):
        if controller_event in self._events:
            current_controller_event = self._events[controller_event]
            if self._controller_event_valid(current_controller_event):
                if controller_event_type == ControllerEventType.PRESS:
                    function = current_controller_event["press"]
                else:
                    function = current_controller_event["release"]
                function(current_controller_event["button"])

    def _controller_event_valid(self, controller_event):
        controller_event_entries = ["press", "release", "button"]
        for controller_event_entry in controller_event_entries:
            if not self._controller_event_entry_valid(controller_event_entry, controller_event):
                return False
        return True

    def _controller_event_entry_valid(self, controller_event_entry, controller_event):
        return controller_event_entry in controller_event and controller_event[controller_event_entry] != None

    def handle_axis_motion_event(self, joystick, x_offset, y_offset):
        x_offset_updated, y_offset_updated = self._handle_axis_motion_event_left_stick(joystick, x_offset, y_offset)
        self._handle_axis_motion_event_right_stick(joystick)
        return x_offset_updated, y_offset_updated

    def _handle_axis_motion_event_left_stick(self, joystick, x_offset, y_offset):
        if self._left_stick_is_mouse:
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            x, y, _, _ = self._filter_axis(x, y)
            x_offset_updated = x * X_OFFSET_MAX
            y_offset_updated = y * Y_OFFSET_MAX
            return x_offset_updated, y_offset_updated
        else:
            return x_offset, y_offset

    def _handle_axis_motion_event_right_stick(self, joystick):
        x = joystick.get_axis(2)
        y = joystick.get_axis(3)
        x, y, x_direction, y_direction = self._filter_axis(x, y)

        if x_direction == ControllerEvent.LEFTRIGHT_CENTERED:
            self._thread_pool[ControllerEvent.LEFT].set_delay(x)
            self._thread_pool[ControllerEvent.RIGHT].set_delay(x)
        else:
            self._thread_pool[x_direction].set_delay(x)

        if y_direction == ControllerEvent.UPDOWN_CENTERED:
            self._thread_pool[ControllerEvent.UP].set_delay(y)
            self._thread_pool[ControllerEvent.DOWN].set_delay(y)
        else:
            self._thread_pool[y_direction].set_delay(y)

    def _filter_axis(self, x, y):
        filtered_x = 0
        filtered_y = 0
        direction_x = ControllerEvent.LEFTRIGHT_CENTERED
        direction_y = ControllerEvent.UPDOWN_CENTERED

        if y <= -0.1:
            # print("up: %0.2f" % y)
            filtered_y = y
            direction_y = ControllerEvent.UP
        if y >= 0.1:
            # print("down: %0.2f" % y)
            filtered_y = y
            direction_y = ControllerEvent.DOWN
        if (y > -0.1) and (y < 0.1):
            # print("y centered: %0.2f" % y)
            filtered_y = 0
            direction_y = ControllerEvent.UPDOWN_CENTERED
        if x <= -0.1:
            # print("left: %0.2f" % x)
            filtered_x = x
            direction_x = ControllerEvent.LEFT
        if x >= 0.1:
            # print("right: %0.2f" % x)
            filtered_x = x
            direction_x = ControllerEvent.RIGHT
        if (x > -0.1) and (x < 0.1):
            # print("x centered: %0.2f" % x)
            filtered_x = 0
            direction_x = ControllerEvent.LEFTRIGHT_CENTERED
        return filtered_x, filtered_y, direction_x, direction_y

    def _add_repeater(self, controller_event, name):
        current_controller_event = self._events[controller_event]
        if self._controller_event_valid(current_controller_event):
            repeater = KeyRepeater(0.0, name, current_controller_event["press"], current_controller_event["release"], current_controller_event["button"])
            repeater.start()
            self._thread_pool[controller_event] = repeater

    def stop(self):
        for repeater in self._thread_pool.values():
            repeater.stop()
            repeater.join()

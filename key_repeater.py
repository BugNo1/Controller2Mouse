import threading
import time

class KeyRepeater(threading.Thread):

    def __init__(self, initial_delay, name, press_function, release_function, button):
        super(KeyRepeater, self).__init__()
        self._min_delay_ms = 10
        self._delay = initial_delay
        self._name = name
        self._press_function = press_function
        self._release_function = release_function
        self._button = button
        self._run = True

    def set_delay(self, delay):
        if delay == 0:
            self._delay = 0
        else:
            self._delay = (self._min_delay_ms / abs(delay)) / 1000.0

    def stop(self):
        self._run = False

    def run(self):
        print("%s started" % self._name)
        while self._run:
            if self._delay != 0:
                #print("%s delay: %s" % (self._name, self._delay))
                self._press_function(self._button)
                self._release_function(self._button)
                time.sleep(self._delay)
            else:
                time.sleep(0.10)  # so that the process is sleeping most of the time
        print("%s ended" % self._name)

from enum import Enum

class ControllerEvent(Enum):
    UP                        = 0
    DOWN                      = 1
    UPDOWN_CENTERED           = 2
    LEFT                      = 3
    RIGHT                     = 4
    LEFTRIGHT_CENTERED        = 5
    CROSS                     = 6
    SQUARE                    = 7
    TRIANGLE                  = 8
    CIRCLE                    = 9
    OPTIONS                   = 10

class ControllerEventType(Enum):
    PRESS                     = 0
    RELEASE                   = 1

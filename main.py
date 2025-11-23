import time
import pygame
from pynput.mouse import Controller, Button

JOYSTICK_1 = 0
JOYSTICK_2 = 1

x_offset_max = 100
y_offset_max = 100
x_offset = 0
y_offset = 0

def handle_button_down_event(event):
    # print(event.button)
    if event.button == 0:  # cross button
        if event.instance_id == JOYSTICK_1:
            mouse.press(Button.left)
    if event.button == 1:  # circle button
        pass
    if event.button == 2:  # square button
        pass
    if event.button == 3:  # triangle button
        if event.instance_id == JOYSTICK_1:
            mouse.press(Button.right)
    if event.button == 6:  # options button
        pass
    if event.button == 11:  # up button
        pass
    if event.button == 12:  # down button
        pass
    if event.button == 13:  # left button
        pass
    if event.button == 14:  # right button
        pass

def handle_button_up_event(event):
    if event.button == 0:  # cross button
        if event.instance_id == JOYSTICK_1:
            mouse.release(Button.left)
    if event.button == 1:  # circle button
        pass
    if event.button == 2:  # square button
        pass
    if event.button == 3:  # triangle button
        if event.instance_id == JOYSTICK_1:
            mouse.release(Button.right)
    if event.button == 6:  # options button
        pass
    if event.button == 11:  # up button
        pass
    if event.button == 12:  # down button
        pass
    if event.button == 13:  # left button
        pass
    if event.button == 14:  # right button
        pass

def handle_axis_motion_event(event):
    joystick = joysticks[event.instance_id]
    # print(event.instance_id)
    x = joystick.get_axis(0)
    y = joystick.get_axis(1)
    if y <= -0.1:
        # print("up: %0.2f" % y)
        y_offset = y * y_offset_max
    if y >= 0.1:
        # print("down: %0.2f" % y)
        y_offset = y * y_offset_max
    if (y > -0.1) and (y < 0.1):
        # print("y centered: %0.2f" % y)
        y_offset = 0
    if x <= -0.1:
        # print("left: %0.2f" % x)
        x_offset = x * x_offset_max
    if x >= 0.1:
        # print("right: %0.2f" % x)
        x_offset = x * x_offset_max
    if (x > -0.1) and (x < 0.1):
        # print("x centered: %0.2f" % x)
        x_offset = 0
    mouse.move(int(x_offset), int(y_offset))

pygame.init()
pygame.joystick.init()
mouse = Controller()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print("Number of Joysticks found: %d" % len(joysticks))

done = False
while not done:
    # Event processing
    # PyGame seems to have an issue with event processing - But when Steam is running everything is fine!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.JOYBUTTONDOWN:
            handle_button_down_event(event)

        if event.type == pygame.JOYBUTTONUP:
            handle_button_up_event(event)

        if event.type == pygame.JOYAXISMOTION:
            handle_axis_motion_event(event)

    time.sleep(0.05)  # needed to not overload the event system


# TODO:
 # circle = ESC
 # triangle = right mouse
 # square = SPACE
 # right joystick = arrow keys (repeat)
 # cross keys on left side = arrow keys - but pressed = pressed and released = released (if possible)
 # control = FN + F5

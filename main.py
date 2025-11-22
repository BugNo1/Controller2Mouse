import time
import pygame
from pynput.mouse import Controller, Button

x_offset_max = 100
y_offset_max = 100
x_offset = 0
y_offset = 0

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
            done = True  # Flag that we are done so we exit this loop.

        if event.type == pygame.JOYBUTTONDOWN:
            #print("Joystick button pressed: %d" % event.button)
            #print()
            if event.button == 0:
                #pyautogui.mouseDown(button='left')
                mouse.press(Button.left)
            if event.button == 2:
                #pyautogui.mouseDown(button='right')
                mouse.press(Button.right)

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                #pyautogui.mouseUp(button='left')
                mouse.release(Button.left)
            if event.button == 2:
                #pyautogui.mouseUp(button='right')
                mouse.release(Button.right)
            #print("Joystick button released: %d" % event.button)
            #print()

        if event.type == pygame.JOYAXISMOTION:
            joystick = joysticks[event.instance_id]
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            if y <= -0.1:
                #print("up: %0.2f" % y)
                y_offset = y * y_offset_max
            if y >= 0.1:
                #print("down: %0.2f" % y)
                y_offset = y * y_offset_max
            if (y > -0.1) and (y < 0.1):
                #print("y centered: %0.2f" % y)
                y_offset = 0
            if x <= -0.1:
                #print("left: %0.2f" % x)
                x_offset = x * x_offset_max
            if x >= 0.1:
                #print("right: %0.2f" % x)
                x_offset = x * x_offset_max
            if (x > -0.1) and (x < 0.1):
                #print("x centered: %0.2f" % x)
                x_offset = 0

    mouse.move(int(x_offset), int(y_offset))
    time.sleep(0.05)


# TODO:
 # circle = ESC
 # triangle = right mouse
 # square = SPACE
 # right joystick = arrow keys (repeat)
 # cross keys on left side = arrow keys - but pressed = pressed and released = released (if possible)

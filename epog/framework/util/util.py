import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORIGIN = (0, 0)
SCREEN_RECT = (1280, 720)
LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3


def quit_func(*args, **kwargs):
    pygame.quit()
    sys.exit()

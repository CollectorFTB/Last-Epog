import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORIGIN = (0, 0)
SCREEN_RECT = (1280, 720)
LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3


def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.pixels3d(surface)
    mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
    mean_arr3d = mean_arr[..., np.newaxis]
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    return pygame.surfarray.make_surface(new_arr)

def quit_func(*args, **kwargs):
    pygame.quit()
    sys.exit()

import json
import pygame
import sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORIGIN = (0, 0)
ORIGINAL_RECT = (1920, 1080)
DEFAULT_SCREEN_RECT = (1280, 720)
LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3
SCROLL_UP = 4
SCROLL_DOWN = 5

def open_scraped_data(item_path):
    with open(f'../wiki_scraper/output/{item_path}.json', 'r') as f:
        return json.load(f)


def group_by_value(data, key):
    data = sorted(data, key=key)
    i = 0
    groups = []
    
    while i <= len(data) - 1:
        value = key(data[i])
        groups.append([elem for elem in data if key(elem) == value])
        i = data.index(groups[-1][-1]) + 1
    return groups


def blit_text(surface, line, rect, font, color=pygame.Color('black')):
    """tweaked version of https://stackoverflow.com/a/42015712"""
    words = [word for word in line.split(' ')]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = rect.width, rect.height
    x, y = rect.left, rect.top
    cur_width = 0
    for word in words:
        word_surface = font.render(word, 0, color)
        word_width, word_height = word_surface.get_size()
        if cur_width + word_width >= max_width:
            cur_width = 0
            x = rect.left  # Reset the x.
            y += word_height  # Start on new row.
        surface.blit(word_surface, (x + cur_width, y))
        cur_width += word_width + space


def greyscale(surface: pygame.Surface):
    arr = pygame.surfarray.pixels3d(surface)
    mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
    mean_arr3d = mean_arr[..., np.newaxis]
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    return pygame.surfarray.make_surface(new_arr)

def quit_func(*args, **kwargs):
    pygame.quit()
    sys.exit()

def list_mul(l, m):
    print(l, m)
    return [int(element * m) for element in l]

def list_add(l, a):
    return [element + a for element in l]

def is_scroll_click(button):
    return button in [SCROLL_DOWN, SCROLL_UP]

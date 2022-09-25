from operator import attrgetter
from framework.util.util import SCREEN_RECT
from framework.button.rotating_button import RotatingButton
from framework.screen import Screen
from framework.logic.idols import IDOL_GRID
from functools import partial
from copy import deepcopy
import pygame

# calculated once dont question it
GRID_ORIGIN = (SCREEN_RECT[1] * 104/720, SCREEN_RECT[1] * 132 / 720, SCREEN_RECT[1] * 103/720, SCREEN_RECT[1] * 4/720)

def embed_affix_buttons(func, affix_buttons):
    def _idol_callback(button, *args, **kwargs):
        prefix_button, suffix_button = affix_buttons
        rv = func(button, *args, **kwargs)
        prefix_button.objects, prefix_button.value = button.objects[button.value].all_prefixes, 0
        suffix_button.objects, prefix_button.value = button.objects[button.value].all_suffixes, 0
        return rv
    return _idol_callback


def pos_to_grid(mouse_pos):
    left, top, length, gap = GRID_ORIGIN
    left, top, length, gap = int(left), int(top), int(length), int(gap)
    right, bottom = left + length, top + length
    import ipdb

    # ipdb.set_trace()
    try:
        j = next(i for i in range(5) if mouse_pos[0] in range(left + i*(gap+length), right + bottom*(gap+length)))
        i = next(i for i in range(5) if mouse_pos[1] in range(top + i*(gap+length), bottom + i*(gap+length)))
    except StopIteration:
        return None
    
    return i, j


class IdolScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.value = 0
        super().__init__(*args, **kwargs)

        self.grid = deepcopy(IDOL_GRID)
        self.idol_button.callback = embed_affix_buttons(RotatingButton._callback, self.affix_buttons)

    @property
    def affix_buttons(self):
        return [button for button in self.buttons if 'Prefix' in button.name or 'Suffix' in button.name]

    @property
    def idol_button(self):
        return next(button for button in self.buttons if 'Idol' in button.name)
        
    def _load_button_objects(self, button_objects):
        self.all_idols = button_objects['Idols']('Sentinel')

        for button in self.empty_buttons:
            name, index = button.name.split('-')
            
            if name == 'Prefix':
                button.objects = self.all_idols[self.value].all_prefixes
            elif name == 'Suffix':
                button.objects = self.all_idols[self.value].all_suffixes
            elif name == 'Idol':
                button.objects = self.all_idols
                button.key = attrgetter('name')

    def handle_mouse_down_event(self, event, debug):
        rv =  super().handle_mouse_down_event(event, debug)
        
        if self.idol_button.check_collision(pygame.mouse.get_pos()):
            self.dragging = True
        
        return rv

    def handle_mouse_up_event(self, event, debug):
        rv = super().handle_mouse_up_event(event, debug)
        x,y = pygame.mouse.get_pos()
        grid_pos = pos_to_grid((x - self.origin[0], y))
        if grid_pos and self.dragging:
            print('lock on: ', grid_pos)
        
        self.dragging = False
        return rv
"""
idol_type rotating button
idol_prefix rotating button
idol_suffix rotating button
created_item button
"""
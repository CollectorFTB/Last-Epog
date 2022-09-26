from operator import attrgetter
from framework.logic.item_db import get_image_from_db
from framework.util.util import SCREEN_RECT
from framework.button.rotating_button import RotatingButton
from framework.screen import Screen
from framework.logic.idols import IDOL_GRID, put_on_grid, fit_into_grid, remove_from_grid
from functools import partial
from copy import deepcopy
import pygame

"""
TODO: 
idol images ~
put image to grid after lock on
"""

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
        j = next(i for i in range(5) if mouse_pos[0] in range(left + i*(gap+length), right + i*(gap+length)))
        i = next(i for i in range(5) if mouse_pos[1] in range(top + i*(gap+length), bottom + i*(gap+length)))
    except StopIteration:
        return None
    
    return i, j

def grid_to_pos(grid_pos):
    left, top, length, gap = GRID_ORIGIN
    left, top, length, gap = int(left), int(top), int(length), int(gap)

    return left + grid_pos[1] * (gap + length), top + grid_pos[1] * (gap + length)

class IdolScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.value = 0
        super().__init__(*args, **kwargs)

        self.grid = deepcopy(IDOL_GRID)
        self.locked_idols = []
        self.dragged_locked_pos = None
        self.idol_button.callback = embed_affix_buttons(RotatingButton._callback, self.affix_buttons)

    @property
    def affix_buttons(self):
        return [button for button in self.buttons if 'Prefix' in button.name or 'Suffix' in button.name]

    @property
    def trash_button(self):
        return next(button for button in self.buttons if 'Trash' == button.name)

    @property
    def idol_button(self):
        return next(button for button in self.buttons if 'Idol' in button.name)
    
    @property
    def prefix_button(self):
        return next(button for button in self.buttons if 'Prefix' in button.name)
    
    @property
    def suffix_button(self):
        return next(button for button in self.buttons if 'Suffix' in button.name)

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

    def draw_buttons(self, debug=False):
        rv =  super().draw_buttons(debug)

        for idol, _, _ in self.locked_idols:
            image = get_image_from_db(idol.name)
            for i,row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if cell == idol:
                        origin = grid_to_pos((i, j))
                        origin = self.origin[0] + origin[0], self.origin[1] + origin[1]
                        self.surface.blit(image, origin)
                        

        return rv

    def handle_mouse_down_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()
        
        if (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
            if clicked_button.click_rv:
                return clicked_button.click_rv
        
        x,y = mouse_pos
        grid_pos = pos_to_grid((x - self.origin[0], y))
        
        if grid_pos and not isinstance(self.grid[grid_pos[0]][grid_pos[1]], int):
            self.dragged_locked_pos = grid_pos

        if self.idol_button.check_collision(mouse_pos):
            self.dragging = True
        

    def handle_mouse_up_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()
        
        if (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
            if clicked_button.callback:
                clicked_button.callback(mouse=event.button, screen=self, button=clicked_button)
        
        x,y = mouse_pos
        grid_pos = pos_to_grid((x - self.origin[0], y))
        if grid_pos and self.dragging:
            idol = self.idol_button.current_object
            if fit_into_grid(self.grid, grid_pos[0], grid_pos[1], idol):
                put_on_grid(self.grid, grid_pos[0], grid_pos[1], idol)
                self.locked_idols.append((idol, self.prefix_button.value, self.suffix_button.value))

                print([li[1:] for li in self.locked_idols])
        
        if self.dragged_locked_pos and self.trash_button.check_collision(mouse_pos):
            i, j = self.dragged_locked_pos
            idol = self.grid[i][j].__repr__.__self__
            remove_from_grid(self.grid, i, j, idol)
            locked_idol = next(elem for elem in self.locked_idols if elem[0] == idol)
            self.locked_idols.remove(locked_idol)
            
            
        self.dragged_locked_pos = None
        self.dragging = False
"""
idol_type rotating button
idol_prefix rotating button
idol_suffix rotating button
created_item button
"""
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
GRID_ORIGIN = (SCREEN_RECT[1] * 104/720, SCREEN_RECT[1] * 128 / 720, SCREEN_RECT[1] * 103/720, SCREEN_RECT[1] * 4/720)

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
    
    try:
        j = next(i for i in range(5) if mouse_pos[0] in range(left + i*(gap+length), right + i*(gap+length)))
        i = next(i for i in range(5) if mouse_pos[1] in range(top + i*(gap+length), bottom + i*(gap+length)))
    except StopIteration:
        return None
    
    return i, j

def grid_to_pos(grid_pos):
    left, top, length, gap = GRID_ORIGIN
    left, top, length, gap = int(left), int(top), int(length), int(gap)

    return left + grid_pos[1] * (gap + length), top + grid_pos[0] * (gap + length)

class IdolScreen(Screen):
    def __init__(self, *args, **kwargs):
        self.value = 0
        super().__init__(*args, **kwargs)

        self.grid = deepcopy(IDOL_GRID)
        self.locked_idols = []
        self.locked_positions = []
        self.dragged_locked_idol = None
        self.idol_button.callback = embed_affix_buttons(RotatingButton._callback, self.button_with_name('fix'))

    @property
    def idol_button(self):
        return next(button for button in self.buttons if 'Idol' in button.name)

    def _load_button_objects(self, button_objects):
        self.all_idols = button_objects['Idols']('Sentinel')

        self.button_with_name('Prefix').objects = self.all_idols[self.value].all_prefixes
        self.button_with_name('Suffix').objects = self.all_idols[self.value].all_suffixes
        self.idol_button.objects = self.all_idols
        self.idol_button.key = attrgetter('name')

    def draw_buttons(self, debug=False):
        rv =  super().draw_buttons(debug)

        _, _, width, gap = GRID_ORIGIN
        for position, (idol, _, _) in zip(self.locked_positions, self.locked_idols):
            i,j = position
            image = get_image_from_db(idol.name, (idol.width * (width + gap) - gap, idol.height * (width + gap) - gap))
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
        
        if grid_pos and not isinstance((idol := self.grid[grid_pos[0]][grid_pos[1]]), int):
            print('draggin!')
            self.dragged_locked_idol = idol.__repr__.__self__

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
                self.locked_positions.append(grid_pos)
                self.locked_idols.append((idol, self.button_with_name('Prefix').value, self.button_with_name('Suffix').value))
        
        if self.dragged_locked_idol and self.button_with_name('Trash').check_collision(mouse_pos):
            index, locked_idol, pos = next((index, i, p) for index, (i, p) in enumerate(zip(self.locked_idols, self.locked_positions)) if i[0] is self.dragged_locked_idol)
            i, j = pos
            remove_from_grid(self.grid, i, j, locked_idol[0])
            self.locked_idols.remove(locked_idol)
            self.locked_positions.remove(self.locked_positions[index])
            
        self.dragged_locked_idol = None
        self.dragging = False
"""
idol_type rotating button
idol_prefix rotating button
idol_suffix rotating button
created_item button
"""
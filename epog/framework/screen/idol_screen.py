from operator import attrgetter
from framework.screen import Screen
from framework.button.rotating_button import RotatingButton
from framework.logic.item_db import get_image_from_db
from framework.logic.idols import IDOL_GRID, put_on_grid, fit_into_grid, remove_from_grid
from copy import deepcopy
import pygame


GRID_ORIGIN = (156, 192, 154, 6)

def embed_affix_buttons(func, affix_buttons):
    def _idol_callback(button, *args, **kwargs):
        prefix_button, suffix_button = affix_buttons
        rv = func(button, *args, **kwargs)
        prefix_button.load_affixes(button.objects[button.value].all_prefixes)
        suffix_button.load_affixes(button.objects[button.value].all_suffixes)
        return rv
    return _idol_callback


def pos_to_grid(mouse_pos, grid_origin):
    left, top, length, gap = grid_origin
    right, bottom = left + length, top + length
    
    try:
        j = next(i for i in range(5) if mouse_pos[0] in range(left + i*(gap+length), right + i*(gap+length)))
        i = next(i for i in range(5) if mouse_pos[1] in range(top + i*(gap+length), bottom + i*(gap+length)))
    except StopIteration:
        return None
    
    return i, j

def grid_to_pos(grid_pos, grid_origin):
    left, top, length, gap = grid_origin
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
    def idol_origin(cls):
        return [cls.scale_size(coord) for coord in GRID_ORIGIN]

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

        _, _, width, gap = self.idol_origin
        for position, (idol, _, _, _, _) in zip(self.locked_positions, self.locked_idols):
            i,j = position
            image = get_image_from_db(idol.name, (idol.width * (width + gap) - gap, idol.height * (width + gap) - gap))
            origin = grid_to_pos((i, j), self.idol_origin)
            origin = self.origin[0] + origin[0], self.origin[1] + origin[1]
            self.surface.blit(image, origin)


        return rv

    def handle_mouse_down_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()
        
        if (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
            if clicked_button.click_rv:
                return clicked_button.click_rv
        
        x,y = mouse_pos
        grid_pos = pos_to_grid((x - self.origin[0], y), self.idol_origin)
        
        if grid_pos and not isinstance((idol := self.grid[grid_pos[0]][grid_pos[1]]), int):
            self.dragged_locked_idol = idol.__repr__.__self__
            self.dragged_locked_idol_pos = grid_pos

        if self.idol_button.check_collision(mouse_pos):
            self.dragging = True
        

    def handle_mouse_up_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()
        prefix_button, suffix_button = self.button_with_name('fix')
        
        x,y = mouse_pos
        grid_pos = pos_to_grid((x - self.origin[0], y), self.idol_origin)
        if grid_pos and self.dragging:
            idol = self.idol_button.current_object
            if fit_into_grid(self.grid, grid_pos[0], grid_pos[1], idol):
                put_on_grid(self.grid, grid_pos[0], grid_pos[1], idol)
                self.locked_positions.append(grid_pos)
                self.locked_idols.append((idol, prefix_button.value, suffix_button.value, prefix_button.current_roll, suffix_button.current_roll))
        
        elif self.dragged_locked_idol: 
            if self.button_with_name('Trash').check_collision(mouse_pos) or (idol_edit := self.button_with_name('Idol').check_collision(mouse_pos)):
                index = self.locked_positions.index(self.dragged_locked_idol_pos)
                i, j = self.dragged_locked_idol_pos
                
                if idol_edit:
                    idol_to_edit = self.locked_idols[index]
                    idol_button = self.button_with_name('Idol')
                    idol_button.value = idol_button.objects.index(idol_to_edit[0])
                    
                    prefix_button.load_affixes(idol_button.objects[idol_button.value].all_prefixes)
                    suffix_button.load_affixes(idol_button.objects[idol_button.value].all_suffixes)
                    
                    prefix_button.value, prefix_button.current_roll = idol_to_edit[1], idol_to_edit[3]
                    suffix_button.value, suffix_button.current_roll = idol_to_edit[2], idol_to_edit[4]


                remove_from_grid(self.grid, i, j, self.dragged_locked_idol)
                self.locked_idols.remove(self.locked_idols[index])
                self.locked_positions.remove(self.locked_positions[index])


        elif (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
            if clicked_button.callback:
                clicked_button.callback(mouse=event.button, screen=self, button=clicked_button)
        

        self.dragged_locked_idol = None
        self.dragging = False
"""
idol_type rotating button
idol_prefix rotating button
idol_suffix rotating button
created_item button
"""
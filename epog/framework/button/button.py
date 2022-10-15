from dataclasses import dataclass

import pygame

@dataclass
class Rect:
    left: int
    right: int
    top: int
    bottom: int
    
    def __init__(self, left, top, right=None, bottom=None, width=None, height=None):
        self.left = left
        self.top = top
        
        if right is not None and bottom is not None:
            self.right = right
            self.bottom = bottom
        else:
            self.right = self.left + width
            self.bottom = self.top + height
    
    @property
    def width(self):
        return (self.right - self.left)

    @property
    def height(self):
        return (self.bottom - self.top)

    @property
    def center(self):
        return self.left + self.width//2, self.top + self.height//2


class Button:
    RATIO = 1

    @classmethod 
    def to_raw(cls, value):
        return int(value / cls.RATIO)

    @classmethod
    def scale_size(cls, value):
        return int(value * cls.RATIO)

    def refresh(self):
        left, top, right, bottom = self.original_values
        w, h = Button.scale_size(right-left), Button.scale_size(bottom-top)
        self.rect = Rect(Button.scale_size(left), Button.scale_size(top), width=w, height=h)

    def __init__(self, pos, width=50, height=50, callback=None, click_rv=None, name=None):
        x,y = pos
        self.rect = Rect(x, y, width=width, height=height)
        self.original_values = [Button.to_raw(self.rect.left), Button.to_raw(self.rect.top), Button.to_raw(self.rect.right), Button.to_raw(self.rect.bottom)]
        self.name = name
        self.callback = callback
        self.click_rv = click_rv
                
    def draw(self, screen, debug):
        if debug:
            pygame.draw.rect(screen, (0, 100, 255), (self.rect.left, self.rect.top, self.rect.width, self.rect.height), 3)
        

    def check_collision(self, position) -> bool:
        x,y = position
        return x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom)
    
    def hover(self, surface):
        pass

    def scroll(self, button):
        pass

    def toggle(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.callback(self, *args, **kwargs) if self.callback else None

    def to_dict(self):
        left, top, right, bottom = self.original_values
        temp_button = Button((left, top), right-left, bottom-top, name=self.name)
        del temp_button.original_values
        temp_button.rect = temp_button.rect.__dict__
        temp_button.type = Button.__name__
        return temp_button.__dict__
    
    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == Button.__name__
        del button_dict['type']

        orig_rect = button_dict['rect']
        new_button = cls(pos=(Button.scale_size(orig_rect['left']), Button.scale_size(orig_rect['top'])), 
                    width=Button.scale_size(orig_rect['right']) - Button.scale_size(orig_rect['left']), 
                    height=Button.scale_size(orig_rect['bottom']) - Button.scale_size(orig_rect['top']), 
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'])
        new_button.original_values = [orig_rect['left'], orig_rect['top'], orig_rect['right'], orig_rect['bottom']]
        return new_button

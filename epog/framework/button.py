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
        return self.width//2, self.height//2


class Button:
    def __init__(self, pos, width=50, height=50, callback=None, click_rv=None, name=None):
        x,y = pos
        self.rect = Rect(x, y, width=width, height=height)
        self.name = name
        self.callback = callback
        self.click_rv = click_rv
                
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 100, 255), (self.rect.left, self.rect.top, self.rect.width, self.rect.height), 3)

    def update(self, screen):
        pass

    def checkForInput(self, position) -> bool:
        x,y = position
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def __call__(self, *args, **kwargs):
        return self.callback(self, *args, **kwargs) if self.callback else None

    def to_dict(self):
        temp_button = Button((self.rect.left, self.rect.top), self.rect.width, self.rect.height, name=self.name)
        temp_button.rect = temp_button.rect.__dict__
        temp_button.type = Button.__name__
        return temp_button.__dict__
    
    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == Button.__name__
        del button_dict['type']
        
        return cls((button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'], 
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'])

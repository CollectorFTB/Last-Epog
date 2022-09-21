import pdb
import pygame

from framework.button import Button
from framework.button.button import Rect
font = lambda size: pygame.font.Font('assets/font.ttf', size)

class TextButton(Button):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text 
    
    def draw(self, surface, debug):
        super().draw(surface, debug)
        text = font(self.rect.width//len(self.text)).render(self.text, True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=self.rect.center))


    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = TextButton.__name__
        temp_button_dict['text'] = self.text
        return temp_button_dict
    
    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == TextButton.__name__
        del button_dict['type']
        
        return cls(pos=(button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'],
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'],
                    text=button_dict['text'])

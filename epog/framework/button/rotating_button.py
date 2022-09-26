import os
import pygame
from operator import attrgetter, itemgetter

from framework.button.button import Rect
from framework.label.label import Label
from framework.button.button import Button
from framework.util.util import to_current
from framework.logic.item_db import item_db, get_image_from_db

class RotatingButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 0
        self.objects = []
        self.image = None
        self.callback = self._callback
        self.key = itemgetter('implicit') if 'Blessing' in self.name else attrgetter('name') 

    def hover(self, surface):
        pass
        Label(Rect(self.rect.left - 50 , self.rect.bottom, self.rect.right + 150, self.rect.bottom), self.key(self.objects[self.value])).draw(surface, slide=True)

    @property
    def current_object(self):
        return self.objects[self.value]


    def draw(self, screen: pygame.surface.Surface, debug):
        super().draw(screen, debug)
    
        try:
            if self.current_object.name in item_db:
                screen.blit(get_image_from_db(self.current_object.name), (self.rect.left, self.rect.top))
        except:
            pass


    def _callback(self, *args, **kwargs):
        try:
            mouse = kwargs['mouse']
        except:
            return
            
        self.value = self.value - mouse + 2
        if self.value >= len(self.objects):
            self.value = 0
        elif self.value < 0:
            self.value = len(self.objects) - 1

    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = RotatingButton.__name__
        return temp_button_dict


    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == RotatingButton.__name__
        del button_dict['type']

        orig_rect = button_dict['rect']
        new_button = cls(pos=(to_current(orig_rect['left']), to_current(orig_rect['top'])), 
                    width=to_current(orig_rect['right']) - to_current(orig_rect['left']), 
                    height=to_current(orig_rect['bottom']) - to_current(orig_rect['top']), 
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'])

        new_button.original_values = [orig_rect['left'], orig_rect['top'], orig_rect['right'], orig_rect['bottom']]
        return new_button
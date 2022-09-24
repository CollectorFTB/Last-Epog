from framework.button import CounterButton
from framework.label.label import Label
from framework.button.button import Rect
from framework.util.util import BLACK, LEFT_CLICK
import pygame

class PassiveTreeButton(CounterButton):
    def __init__(self, stats, required_passives, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = stats
        self.required_passives = required_passives
        
    def draw(self, surface: pygame.surface.Surface, debug, show_counter=True):
        super().draw(surface, debug)
        
        if show_counter:
            black_rect = pygame.rect.Rect(self.rect.left, self.rect.bottom-24, self.rect.width, 24)
            surface.fill(BLACK, black_rect)
            Label(black_rect, f'{self.value}/{self.max}').draw(surface)
    
    def hover(self, surface):
        Label(Rect(self.rect.right, self.rect.top -50, self.rect.right + 200, self.rect.bottom + 50), self.name).draw(surface)

    
    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = PassiveTreeButton.__name__
        temp_button_dict['stats'] = self.stats
        temp_button_dict['required_passives'] = self.required_passives
        return temp_button_dict
    
    def _is_unlocked(self):
        # overriden in PassiveTreeScreen
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == PassiveTreeButton.__name__
        del button_dict['type']
        
        return cls(pos=(button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'],
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'],
                    max=button_dict['max'],
                    stats=button_dict['stats'],
                    required_passives=button_dict['required_passives'])

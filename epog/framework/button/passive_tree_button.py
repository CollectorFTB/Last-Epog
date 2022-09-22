from framework.button import CounterButton
from framework.util.util import BLACK, LEFT_CLICK
import pygame

class PassiveTreeButton(CounterButton):
    def __init__(self, stats, required_passives, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = stats
        self.required_passives = required_passives
        
    def draw(self, surface: pygame.surface.Surface, debug):
        super().draw(surface, debug)
        black_rect = pygame.rect.Rect(self.rect.left, self.rect.bottom-18, self.rect.width, 18)
        surface.fill(BLACK, black_rect)
    
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
from framework.button import RotatingButton
from framework.util.util import WHITE
from framework.util.font import font

class AffixButton(RotatingButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, surface, debug):
        super().draw(surface, debug)
        raw_text = self.objects[self.value].name
        text = font(self.rect.width//len(raw_text)).render(raw_text, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def hover(self, *args):
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
        temp_button_dict['type'] = AffixButton.__name__
        return temp_button_dict


    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == AffixButton.__name__
        del button_dict['type']

        orig_rect = button_dict['rect']
        new_button = cls(pos=(AffixButton.scale_size(orig_rect['left']), AffixButton.scale_size(orig_rect['top'])), 
                    width=AffixButton.scale_size(orig_rect['right']) - AffixButton.scale_size(orig_rect['left']), 
                    height=AffixButton.scale_size(orig_rect['bottom']) - AffixButton.scale_size(orig_rect['top']), 
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'])

        new_button.original_values = [orig_rect['left'], orig_rect['top'], orig_rect['right'], orig_rect['bottom']]
        return new_button
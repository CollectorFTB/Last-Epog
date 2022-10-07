from framework.button import Button
from framework.util.font import font
from framework.util.util import WHITE, GREEN

class TextButton(Button):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text 
        self.color = WHITE
    
    def draw(self, surface, debug):
        super().draw(surface, debug)
        text = font(self.rect.width//len(self.text)).render(self.text, True, self.color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def toggle(self):
        if self.color == WHITE:
            self.color = GREEN
        else:
            self.color = WHITE
    
    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = TextButton.__name__
        temp_button_dict['text'] = self.text
        return temp_button_dict
    
    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == TextButton.__name__
        del button_dict['type']
        
        orig_rect = button_dict['rect']
        new_button = cls(pos=(TextButton.scale_size(orig_rect['left']), TextButton.scale_size(orig_rect['top'])), 
                    width=TextButton.scale_size(orig_rect['right']) - TextButton.scale_size(orig_rect['left']), 
                    height=TextButton.scale_size(orig_rect['bottom']) - TextButton.scale_size(orig_rect['top']), 
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'],
                    text=button_dict['text'])
        
        new_button.original_values = [orig_rect['left'], orig_rect['top'], orig_rect['right'], orig_rect['bottom']]
        return new_button

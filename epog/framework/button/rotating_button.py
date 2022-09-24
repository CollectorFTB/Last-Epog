from framework.button.button import Rect
from framework.label.label import Label
from framework.button.button import Button


class RotatingButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 0
        self.objects = []
        self.callback = self._callback

    def hover(self, surface):
        pass
        Label(Rect(self.rect.left - 300, self.rect.bottom - 30, self.rect.right + 300, self.rect.bottom+70), self.objects[self.value]['implicit']).draw(surface)

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

        return cls(pos=(button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'],
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'])
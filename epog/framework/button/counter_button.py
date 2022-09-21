from framework.button import Button
from framework.util.util import LEFT_CLICK

class CounterButton(Button):
    def __init__(self, initial, max, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial = initial
        self.value = initial
        self.max = max
        self.callback = self._callback

    def _is_unlocked(self, *args):
        return True

    def _callback(self, *args, **kwargs):
        try:
            mouse = kwargs['mouse']
        except:
            return
            
        if self._is_unlocked(self):
            print('Allocated!')
            return self._increment() if mouse == LEFT_CLICK else self._decrement()
        print('Cant allocate :(', self.value, self.name, self.required_passives)

    def _increment(self):
        self.value = min(self.max, self.value + 1)

    def _decrement(self):
        self.value = max(self.value - 1, 0)
    
    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = CounterButton.__name__
        temp_button_dict['initial'] = self._initial
        temp_button_dict['max'] = self.max
        return temp_button_dict


    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == CounterButton.__name__
        del button_dict['type']
        
        return cls(pos=(button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'],
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'],
                    initial=button_dict['initial'],
                    max=button_dict['max'])

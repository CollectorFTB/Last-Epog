from framework.button.passive_tree_button import PassiveTreeButton


class BlessingButton(PassiveTreeButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, surface, *args, **kwargs):
        super().draw(surface, *args, **kwargs)

    
    def to_dict(self):
        temp_button_dict = super().to_dict()
        temp_button_dict['type'] = BlessingButton.__name__
        temp_button_dict['stats'] = self.stats
        del temp_button_dict['max']
        del temp_button_dict['required_passives']
        return temp_button_dict
    
    def _is_unlocked(self):
        return True

    @classmethod
    def from_dict(cls, button_dict):
        assert button_dict['type'] == BlessingButton.__name__
        del button_dict['type']
        
        return cls(pos=(button_dict['rect']['left'], button_dict['rect']['top']), 
                    width=button_dict['rect']['right'] - button_dict['rect']['left'], 
                    height=button_dict['rect']['bottom'] - button_dict['rect']['top'],
                    callback=button_dict['callback'], 
                    click_rv=button_dict['click_rv'], 
                    name=button_dict['name'],
                    max=1,
                    stats=button_dict['stats'],
                    required_passives=0)

    
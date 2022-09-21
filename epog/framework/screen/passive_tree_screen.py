from framework.screen import Screen
from framework.button import PassiveTreeButton
from operator import attrgetter

class PassiveTreeScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fix_passive_buttons()
        
    @property
    def passive_tree_buttons(self):
        button_list = list(filter(lambda b: isinstance(b, PassiveTreeButton), self.buttons))
        button_list.sort(key=attrgetter('required_passives'))
        return button_list
    
    def _fix_passive_buttons(self):
        def _is_unlocked(button: PassiveTreeButton):
            total_points = 0
            for b in self.passive_tree_buttons:
                if b.required_passives >= button.required_passives:
                    return total_points >= button.required_passives
                
                total_points += b.value
            
            return False
        
        for button in self.passive_tree_buttons:
            button._is_unlocked = _is_unlocked
        

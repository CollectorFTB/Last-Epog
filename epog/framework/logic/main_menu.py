import json
from framework.util.util import quit_func
from framework.screen import Screen, PassiveTreeScreen

GLOBAL_SCREEN_NAMES = ['Sentinel', 'Void Knight', 'Paladin', 'Forge Guard']

def save_state(**kwargs):
    try:
        parent_screen = kwargs['screen']
    except:
        print('error saving')
        return 

    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    passive_state = {button.name: button.value for screen in passive_tree_screens for button in screen.passive_tree_buttons}
    with open(f'saves/autosave', 'w') as f:
        json.dump(passive_state, f)

def load_state(**kwargs):
    try:
        parent_screen = kwargs['screen']
    except:
        print('error loading')
        return 

    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    with open(f'saves/autosave', 'r') as f:
        passive_data = json.load(f)

    for screen in passive_tree_screens:
        for button in screen.passive_tree_buttons:
            if button.name in passive_data:
                button.value = passive_data[button.name]




main_menu = {
    'quit': quit_func,
    'save': save_state,
    'load': load_state,
}
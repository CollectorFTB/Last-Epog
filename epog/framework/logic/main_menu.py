import json
from framework.util.util import quit_func
from framework.screen import Screen, PassiveTreeScreen

GLOBAL_SCREEN_NAMES = ['Sentinel', 'Void Knight', 'Paladin', 'Forge Guard']
BLESSING_SCREEN_NAME = ['Blessing']

def save_passive_tree():
    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    return {button.name: button.value for screen in passive_tree_screens for button in screen.passive_tree_buttons}
    

def save_state(**kwargs):
    try:
        parent_screen = kwargs['screen']
    except:
        print('error saving')
        return 

    state = {}
    state['passive_tree'] = save_passive_tree()
    
    with open(f'saves/autosave', 'w') as f:
        json.dump(state, f)

def load_passive_tree(passive_tree_save):
    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    for screen in passive_tree_screens:
        for button in screen.passive_tree_buttons:
            if button.name in passive_tree_save:
                button.value = passive_tree_save[button.name]


def load_state(**kwargs):
    try:
        parent_screen = kwargs['screen']
    except:
        print('error loading')
        return 

    with open(f'saves/autosave', 'r') as f:
        state = json.load(f)
    
    load_passive_tree(state['passive_tree'])

    




main_menu = {
    'quit': quit_func,
    'save': save_state,
    'load': load_state,
}
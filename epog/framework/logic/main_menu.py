from framework.util.util import quit_func
from framework.screen import Screen, PassiveTreeScreen

GLOBAL_SCREEN_NAMES = ['Sentinel', 'Void Knight', 'Paladin', 'Forge Guard']

def save_state(**kwargs):
    try:
        screen = kwargs['screen']
    except:
        return

    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    for screen in passive_tree_screens:
        for button in screen.passive_tree_buttons:
            print(button.name, button.value)


main_menu = {
    'quit': quit_func,
    'save': save_state
}
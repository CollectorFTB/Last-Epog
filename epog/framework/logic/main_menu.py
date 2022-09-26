import json
from sys import prefix
from framework.util.util import quit_func
from framework.screen import Screen, PassiveTreeScreen, idol_screen
from weakref import proxy

GLOBAL_SCREEN_NAMES = ['Sentinel', 'Void Knight', 'Paladin', 'Forge Guard']
BLESSING_SCREEN_NAME = 'Blessings'
IDOL_SCREEN_NAME = 'Idols'

def save_passive_tree():
    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    return {button.name: button.value for screen in passive_tree_screens for button in screen.passive_tree_buttons}
    
def save_blessings():
    blessing_buttons = [button for button in Screen.get_instance(BLESSING_SCREEN_NAME).buttons if 'Blessing' in button.name]
    return {button.name: button.value for button in blessing_buttons}

def save_idols():
    idol_screen = Screen.get_instance(IDOL_SCREEN_NAME)
    saved_idols = []
    for idol, prefix_index, suffix_index in idol_screen.locked_idols:
        saved_idols.append((idol_screen.all_idols.index(idol), prefix_index, suffix_index))

    saved_grid = []
    for i in range(len(idol_screen.grid)):
        row = []
        for j in range(len(idol_screen.grid[i])):
            if (wr := idol_screen.grid[i][j]) in [0, 1]:
                row.append(wr)
            else:
                row.append(next(str(i) for i, (idol, _, _) in enumerate(idol_screen.locked_idols) if idol == wr))

        saved_grid.append(row)
    return (saved_idols, saved_grid)


def save_state(**kwargs):
    state = {}
    state['passive_tree'] = save_passive_tree()
    state['blessings'] = save_blessings()
    state['idols'] = save_idols()
    
    with open(f'saves/autosave', 'w') as f:
        json.dump(state, f)

def load_passive_tree(passive_tree_save):
    passive_tree_screens: list[PassiveTreeScreen] = [Screen.get_instance(name) for name in GLOBAL_SCREEN_NAMES]

    for screen in passive_tree_screens:
        for button in screen.passive_tree_buttons:
            if button.name in passive_tree_save:
                button.value = passive_tree_save[button.name]

def load_blessings(blessings_save):
    for button in Screen.get_instance(BLESSING_SCREEN_NAME).buttons:
        if button.name in blessings_save:
            button.value = blessings_save[button.name]

def load_idols(idols_save):
    loaded_idols, loaded_grid = idols_save
    idol_screen = Screen.get_instance(IDOL_SCREEN_NAME)
    idol_screen.locked_idols.clear()
    for idol_index, prefix_index, suffix_index in loaded_idols:
        idol_screen.locked_idols.append((idol_screen.all_idols[idol_index], prefix_index, suffix_index))

    grid = []
    for i in range(len(loaded_grid)):
        row = []
        for j in range(len(loaded_grid[i])):
            if (wr := loaded_grid[i][j]) in [0, 1]:
                row.append(wr)
            else:
                idol, _, _ = idol_screen.locked_idols[int(wr)]
                row.append(proxy(idol))

        grid.append(row)
    
    
    idol_screen.grid = grid
    from pprint import pprint as pp
    pp(grid)
    pp(idol_screen.locked_idols)


def load_state(**kwargs):
    with open(f'saves/autosave', 'r') as f:
        state = json.load(f)

    load_passive_tree(state['passive_tree'])
    load_blessings(state['blessings'])
    load_idols(state['idols'])

main_menu = {
    'quit': quit_func,
    'save': save_state,
    'load': load_state,
}
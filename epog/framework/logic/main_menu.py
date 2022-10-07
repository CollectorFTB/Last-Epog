import pygame
from copy import deepcopy
import itertools
import json
from framework.logic.idols import IDOL_GRID
from framework.util.util import quit_func, ORIGINAL_RECT
from framework.screen import Screen, PassiveTreeScreen
from framework.button import Button
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

    saved_grid = deepcopy(IDOL_GRID)
    for pos_index, pos in enumerate(idol_screen.locked_positions):
        idol = idol_screen.locked_idols[pos_index][0] 
        i,j = pos
        for _i,_j in itertools.product(range(idol.height), range(idol.width)):
            saved_grid[i + _i][j + _j] = str(pos_index)
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

    idol_screen.locked_positions = [None] * len(idol_screen.locked_idols)
    grid = loaded_grid
    passed = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (wr := grid[i][j]) not in [0, 1]:
                idol, _, _ = idol_screen.locked_idols[int(wr)]
                if wr not in passed:
                    passed.append(wr)
                    idol_screen.locked_positions[int(wr)] = (i, j)
                grid[i][j] = proxy(idol)
                    
    idol_screen.grid = grid


def load_state(**kwargs):
    with open(f'saves/autosave', 'r') as f:
        state = json.load(f)

    load_passive_tree(state['passive_tree'])
    load_blessings(state['blessings'])
    load_idols(state['idols'])

def change_resolution(**kwargs):
    RESOLUTIONS = [(1920, 1080), (1600, 900), (1280, 720)]
    current_ratio = Screen.RATIO
    current_resolution = Screen.RESOLUTION
    resolution_button = Screen.get_instance('MainMenu').button_with_name('Resolution')
    Screen.RESOLUTION = RESOLUTIONS[(RESOLUTIONS.index(current_resolution) + 1) % 3]
    Screen.RATIO = Screen.RESOLUTION[0] / ORIGINAL_RECT[0]
    Button.RATIO = Screen.RATIO
    resolution_button.text = f'{Screen.RESOLUTION[0]}x{Screen.RESOLUTION[1]}'
    new_surface = pygame.display.set_mode(Screen.RESOLUTION)
    for screen in Screen.INSTANCES:
        screen.screen_surface = new_surface
        screen.refresh(Screen.RATIO / current_ratio)

main_menu = {
    'quit': quit_func,
    'save': save_state,
    'load': load_state,
    'Resolution': change_resolution
}
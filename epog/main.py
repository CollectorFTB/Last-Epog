import pygame
from framework.button.text_button import TextButton
from framework.screen.passive_tree_screen import PassiveTreeScreen

from framework.util.util import ORIGIN
from framework.screen import Screen
from framework.logic.screen_buttons import screen_buttons

import sys

pygame.init()

def main():
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Epog")

    main_menu = Screen(name='MainMenu', surface=screen, screen_buttons=screen_buttons, parent=None)

    screens = [
        PassiveTreeScreen(name='Sentinel', surface=screen, background_path='assets/Sentinel.png', screen_buttons=screen_buttons, parent=main_menu),
        PassiveTreeScreen(name='Void Knight', surface=screen, background_path='assets/Void Knight.png', screen_buttons=screen_buttons, parent=main_menu),
        PassiveTreeScreen(name='Paladin', surface=screen, background_path='assets/Paladin.png', screen_buttons=screen_buttons, parent=main_menu),
        PassiveTreeScreen(name='Forge Guard', surface=screen, background_path='assets/Forge Guard.png', screen_buttons=screen_buttons, parent=main_menu),
        Screen(name='Blessings', surface=screen, screen_buttons=screen_buttons, parent=main_menu)

    ]
    Screen.link_screens()

    next_screen = main_menu    
    while (next_screen := next_screen.mainloop(debug=bool(len(sys.argv)-1))):
        pass

if __name__ == '__main__':
    main()
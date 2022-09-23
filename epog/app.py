import os
import sys
import pygame

from framework.util.util import SCREEN_RECT
from framework.screen import Screen, PassiveTreeScreen
from framework.logic.screen_buttons import screen_buttons
from framework.logic.screen_connections import screen_information

class Epog:
    def __init__(self):
        self.screen_surface = pygame.display.set_mode(SCREEN_RECT)
        pygame.display.set_caption("Epog")
        self.screens: list[Screen] = []
        for screen_file in os.listdir('game_screens/data'):
            screen_name = os.path.splitext(screen_file)[0]
            
            screen = eval(screen_information[screen_name]['type'])(name=screen_name, surface=self.screen_surface, screen_buttons=screen_buttons)
            self.screens.append(screen)

        Screen.link_screens()
    
    def run(self):
        next_screen = Screen.get_instance('MainMenu')
        while (next_screen := next_screen.mainloop(debug=bool(len(sys.argv)-1))):
            pass
import pygame
from app import Epog
from framework.button.text_button import TextButton
from framework.screen.passive_tree_screen import PassiveTreeScreen

from framework.util.util import ORIGIN
from framework.screen import Screen
from framework.logic.screen_buttons import screen_buttons

def main():
    pygame.init()

    epog = Epog()
    epog.run()

if __name__ == '__main__':
    main()
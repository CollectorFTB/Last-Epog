import pygame

from framework.button import Button
from framework.util import ORIGIN
from framework.screen import Screen

pygame.init()

def main():
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Epog")

    main_menu = Screen(name='MainMenu', surface=screen, parent=None)

    s = Screen(name='Sentinel', surface=screen, background_path='assets/Sentinel.png', parent=main_menu)
    v = Screen(name='Void Knight', surface=screen, background_path='assets/Void Knight.png', parent=main_menu)
    p = Screen(name='Paladin', surface=screen, background_path='assets/Paladin.png', parent=main_menu)
    fg = Screen(name='Forge Guard', surface=screen, background_path='assets/Forge Guard.png', parent=main_menu)

    main_menu.link_to([s])

    for screen in [s,v,p,fg]:
        screen.link_to([s,v,p,fg])

    next_screen = main_menu    
    while (next_screen := next_screen.mainloop(debug=True)):
        pass

if __name__ == '__main__':
    main()
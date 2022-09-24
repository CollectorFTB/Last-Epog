import pygame
from app import Epog
from framework.logic.idols import get_idols

def main():
    pygame.init()

    epog = Epog()
    epog.run()

if __name__ == '__main__':
    main()
from dataclasses import dataclass

import pygame


@dataclass
class Rect:
    left: int
    right: int
    top: int
    bottom: int
    
    def __init__(self, x, y, right=None, bottom=None, width=None, height=None):
        self.left = x
        self.top = y
        
        if right is not None and bottom is not None:
            self.right = right
            self.bottom = bottom
        else:
            self.right = self.left + width
            self.bottom = self.top + height
    
    @property
    def width(self):
        return (self.right - self.left)

    @property
    def height(self):
        return (self.bottom - self.top)

    @property
    def center(self):
        return self.width//2, self.height//2

class Button():
    def __init__(self, pos, width=50, height=50, callback=None):
        self.x = pos[0]
        self.y = pos[1]
        self.callback = callback
        # self.image = image
        # self.font = font
        # self.base_color, self.hovering_color = base_color, hovering_color
        # self.text_input = text_input
        # self.text = self.font.render(self.text_input, True, self.base_color)
        # if self.image is None:
        # 	self.image = self.text
        self.rect = Rect(self.x, self.y, width=width, height=height)
                
        # self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rect = pygame.draw.rect(screen, (0, 100, 255), (self.rect.left, self.rect.top, self.rect.width, self.rect.height), 3)

    def update(self, screen):
        # if self.image is not None:
        # 	screen.blit(self.image, self.rect)
        # screen.blit(self.text, self.text_rect)
        pass

    def checkForInput(self, position) -> bool:
        x,y = position
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def __call__(self, *args, **kwargs):
        return self.callback(self, *args, **kwargs) if self.callback else None

    # def changeColor(self, position):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
    #         self.text = self.font.render(self.text_input, True, self.hovering_color)
    #     else:
    #         self.text = self.font.render(self.text_input, True, self.base_color)
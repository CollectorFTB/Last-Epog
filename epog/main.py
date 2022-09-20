from turtle import back
import pygame, sys
from button import Button
from sentinel import sentinel_tree

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Epog")

DEBUG = True
ORIGIN = (0, 0)

# def get_font(size): # Returns Press-Start-2P in the desired size
#     return pygame.font.Font("assets/font.ttf", size)

# def passives():
#     while True:
#         PLAY_MOUSE_POS = pygame.mouse.get_pos()

#         screen.fill("black")

#         PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
#         PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
#         screen.blit(PLAY_TEXT, PLAY_RECT)

#         PLAY_BACK = Button(pos=(640, 460), 
#                             text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

#         PLAY_BACK.changeColor(PLAY_MOUSE_POS)
#         PLAY_BACK.update(screen)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
#                     main_menu()

#         pygame.display.update()
    
# def b2_func():
#     while True:
#         OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

#         screen.fill("white")

#         OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
#         OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
#         screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

#         OPTIONS_BACK = Button(image=None, pos=(640, 460), 
#                             text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

#         OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
#         OPTIONS_BACK.update(screen)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
#                     main_menu()

#         pygame.display.update()

def quit_func(*args, **kwargs):
    pygame.quit()
    sys.exit()

def save(buttons):
    for b in buttons:
        print(f'Button(({b.rect.left}, {b.rect.top}), {b.rect.width}, {b.rect.height})')

def passives(button: Button):
    sentinel_tree()
    
    sentinel_skill_tree = pygame.image.load("assets/Sentinel.png")
    sentinel_skill_tree = pygame.transform.scale(sentinel_skill_tree, (1280, 720))
    
    back_button = Button((10, 10), 100, 100)

    buttons = [back_button]

    screen.fill('white')
    screen.blit(sentinel_skill_tree, ORIGIN)
    last_click = None

    while True:
        if DEBUG:
            for button in buttons:
                button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_func()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos = pygame.mouse.get_pos()
                if back_button.checkForInput(menu_mouse_pos):
                    save(buttons)
                    return
                else:
                    if last_click:
                        x1,y1 = menu_mouse_pos
                        x2,y2 = last_click
                        buttons.append(Button((x2, y2), x1-x2, y1-y2))
                        last_click = None
                    else:
                        last_click = menu_mouse_pos
                    print(menu_mouse_pos)

        pygame.display.update()




def b2_func(button: Button):
    print('b2')

def main_menu():
    while True:
        screen.fill('black')

        menu_mouse_pos = pygame.mouse.get_pos()

        b1 = Button((640, 250), callback=passives)
        b2 = Button((640, 400), callback=b2_func)
        quit_button = Button((640, 550), callback=quit_func)
        
        buttons = [b1, b2, quit_button]

        for button in buttons:
            if DEBUG:
                button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_func()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                   if button.checkForInput(menu_mouse_pos):
                        button()

        pygame.display.update()

main_menu()
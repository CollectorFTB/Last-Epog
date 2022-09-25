import json
import weakref
import pygame
import os
from framework.button import Button, CounterButton, PassiveTreeButton, TextButton, RotatingButton, AffixButton
from framework.util.util import LEFT_CLICK, ORIGIN, SCREEN_RECT, greyscale, quit_func, to_orig
from framework.logic.screen_connections import screen_information

class Screen:
    INSTANCES = []
    unhighlight_event = pygame.USEREVENT + 1


    @classmethod
    def get_instance(cls, name):
        return next((screen for screen in cls.INSTANCES if screen.name == name), None) 

    def __init__(self, name, surface, screen_buttons, button_objects):
        self.surface: pygame.surface.Surface = surface
        self.parent: Screen = None
        self.buttons: list[Button] = []
        self.name = name

        try:
            self.colored_image = pygame.image.load(f'assets/{self.name}.png')
            size = SCREEN_RECT
            if screen_information[self.name]['strech'] == 2:
                size = size[1], size[1]

            self.colored_image = pygame.transform.scale(self.colored_image, size)
            self.greyscale_image = greyscale(self.colored_image)
            self.image = self.colored_image
        except FileNotFoundError:
            self.image = None

        try:
            alignment = screen_information[self.name]['align']
            if alignment == 'right':
                self.origin = (self.surface.get_rect().right - self.image.get_rect().width, 0)

        except:
            self.origin = ORIGIN

        self._load_buttons()
        self._load_callbacks(screen_buttons)
        self._load_button_objects(button_objects)

        self.__class__.INSTANCES.append(weakref.proxy(self))


    def _load_buttons(self):
        try:
            with open(f'game_screens/data/{self.name}.json', 'r') as f:
                buttons_data = json.load(f)

            for button_data in buttons_data:
                cls = eval(button_data['type'])       
                self.buttons.append(cls.from_dict(button_data))
        # Screen json doesnt exist, load it without buttons
        except:
            pass
    
    def _load_callbacks(self, screen_buttons):
        for button in self.buttons:
            try:
                button.callback = screen_buttons[self.name][button.name]
            except KeyError: # Button doesn't have a preconfigred callback
                pass
    
    def _load_button_objects(self, button_objects):
        for button in self.empty_buttons:
            category, index = button.name.split('-')
            button.objects = button_objects[category](int(index))

    def _save_buttons(self):
        buttons_to_dump = [button.to_dict() for button in self.buttons]
                
        with open(f'game_screens/data/{self.name}.json', 'w') as f:
            json.dump(buttons_to_dump, f)

    @property
    def empty_buttons(self):
        empty = []
        for button in self.buttons:
            try:
                button.objects
                empty.append(button)
            except:
                pass
        return empty
        
    def _add_new_button(self, last_pos, new_pos):
        x1,y1 = new_pos
        x2,y2 = last_pos
        self.buttons.append(Button(last_pos, x1-x2, y1-y2, name=f'Temp-{x2}:{y2}'))

    def mainloop(self, debug=False):
        return self._mainloop(debug=debug)

    def _mainloop(self, debug=False):
        pygame.display.set_caption(self.name)

        self.last_click = None
        self.row_clicks = []
        self.dragged_button = None
        self.highlighted_buttons = []

        while True:
            self.surface.fill('black')
            if self.image:
                self.surface.blit(self.image, self.origin)

            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                button.draw(self.surface, debug=debug)
                if button.check_collision(mouse_pos):
                    button.hover(self.surface)                            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_func()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (next_screen := self.handle_mouse_down_event(event, debug)):
                        return next_screen

                if event.type == self.unhighlight_event:
                    self.highlighted_buttons[0].toggle()
                    self.highlighted_buttons = self.highlighted_buttons[1:]

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_d:
                        debug = not debug
                    if event.key == pygame.K_s:
                        self._save_buttons()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up_event(event, debug)

            pygame.display.update()
    
    def handle_mouse_up_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()

        if debug and self.dragged_button and not (mouse_pos[0] in range(self.dragged_button.rect.left, self.dragged_button.rect.right) and mouse_pos[1] in range(self.dragged_button.rect.top, self.dragged_button.rect.bottom)):
            w,h = self.dragged_button.rect.width, self.dragged_button.rect.height
            self.dragged_button.rect.left = mouse_pos[0]
            self.dragged_button.rect.right = mouse_pos[0] + w
            self.dragged_button.rect.top = mouse_pos[1]
            self.dragged_button.rect.bottom = mouse_pos[1] + h
            self.dragged_button.original_values = [to_orig(mouse_pos[0]), to_orig(mouse_pos[1]), to_orig(mouse_pos[0] + w), to_orig(mouse_pos[1] + h)]
            self.dragged_button = None

    def handle_mouse_down_event(self, event, debug):
        mouse_pos = pygame.mouse.get_pos()

        if (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
            if debug and event.button == 1:
                self.dragged_button = clicked_button
                self.dragged_position = mouse_pos
                if 'Blessing-' in clicked_button.name:
                    print(clicked_button.name)
                    # clicked_button.name = input(f'Replacing {clicked_button.name}: ')
            else:
                if clicked_button.click_rv:
                    return clicked_button.click_rv
                if clicked_button.callback:
                    clicked_button.callback(mouse=event.button, screen=self, button=clicked_button)
                    clicked_button.toggle()
                    self.highlighted_buttons.append(clicked_button)
                    pygame.time.set_timer(self.unhighlight_event, 200, 1)
        
        elif debug and event.button == 1:
            self.row_clicks.append(mouse_pos)
            if len(self.row_clicks) == 5:
                leftx = self.row_clicks[0][0]
                rightx = self.row_clicks[1][0]
                topy = self.row_clicks[2][1]
                bottomy = self.row_clicks[3][1]
                dx = self.row_clicks[4][0] - leftx
                print(f'left, top, right, buttom, gap', leftx, topy, rightx,bottomy, self.row_clicks[4][0] - rightx)
                for i in range(int(input('row length?'))):
                    self.buttons.append(Button((i * dx + leftx, topy), (rightx-leftx), (bottomy-topy), name=f'Temp-{leftx}:{topy}'))
                self.row_clicks.clear()

        elif debug and event.button == 3:
            if self.last_click:
                self._add_new_button(self.last_click, mouse_pos)
                self.last_click = None
            else:
                self.last_click = mouse_pos
        else:
            self.last_click = None
            print(mouse_pos)


    @classmethod
    def link_screens(cls):
        """Set each screen's buttons with names matching to other existing screens, to redirect to that screen when clicked"""
        for screen_to_match in cls.INSTANCES:
            for button in screen_to_match.buttons:
                if (matching_screen := next((screen for screen in cls.INSTANCES if screen.name == button.name), None)):
                    button.click_rv = matching_screen
                    continue
    
    def __enter__(self):
        pass

    def __exit__(self):
        pass

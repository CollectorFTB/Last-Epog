import json
import weakref
import pygame
import os
from framework.button import Button, CounterButton, PassiveTreeButton, TextButton
from framework.util.util import LEFT_CLICK, ORIGIN, SCREEN_RECT, greyscale, quit_func
from framework.logic.screen_connections import screen_information

class Screen:
    INSTANCES = []

    @classmethod
    def get_instance(cls, name):
        return next((screen for screen in cls.INSTANCES if screen.name == name), None) 

    def __init__(self, name, surface, screen_buttons):
        self.surface: pygame.surface.Surface = surface
        self.parent: Screen = None
        self.buttons: list[Button] = []
        self.name = name

        try:
            self.colored_image = pygame.image.load(f'assets/{self.name}.png')
            self.colored_image = pygame.transform.scale(self.colored_image, SCREEN_RECT)
            self.greyscale_image = greyscale(self.colored_image)
            self.image = self.colored_image
        except:
            self.image = None

        self._load_buttons()
        self._load_callbacks(screen_buttons)

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


    def _save_buttons(self):
        buttons_to_dump = [button.to_dict() for button in self.buttons]
                
        with open(f'game_screens/data/{self.name}.json', 'w') as f:
            json.dump(buttons_to_dump, f)

    def _add_new_button(self, last_pos, new_pos):
        x1,y1 = new_pos
        x2,y2 = last_pos
        self.buttons.append(Button(last_pos, x1-x2, y1-y2, name=f'Temp-{x2}:{y2}'))

    def mainloop(self, debug=False):
        try:
            return self._mainloop(debug=debug)
        finally:
            if debug:
                self._save_buttons()

    def _mainloop(self, debug=False):
        pygame.display.set_caption(self.name)

        last_click = None
        unhighlight_event = pygame.USEREVENT + 1
        highlighted_buttons = []

        while True:
            if self.image:
                self.surface.blit(self.image, ORIGIN)
            else:
                self.surface.fill('black')

            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                button.draw(self.surface, debug=debug)
                if button.check_collision(mouse_pos):
                    button.hover(self.surface)                            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_func()
               
                if event.type == unhighlight_event:
                    highlighted_buttons[0].toggle()
                    highlighted_buttons = highlighted_buttons[1:]

                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    debug = not debug

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (clicked_button := next((button for button in self.buttons if button.check_collision(mouse_pos)), None)):
                            if 'Temp-' in clicked_button.name:
                                # clicked_button.name = input(f'Replacing {clicked_button.name}: ')
                                print(clicked_button.name)
                            if clicked_button.click_rv:
                                return clicked_button.click_rv
                            if clicked_button.callback:
                                clicked_button.callback(mouse=event.button, screen=self)
                                clicked_button.toggle()
                                highlighted_buttons.append(clicked_button)
                                pygame.time.set_timer(unhighlight_event, 200, 1)
                        elif debug:
                            if last_click:
                                self._add_new_button(last_click, mouse_pos)
                                last_click = None
                            else:
                                last_click = mouse_pos
                    else:
                        last_click = None
                        print(mouse_pos)

            pygame.display.update()
    
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

import json
import weakref
import pygame
from framework.button import Button, CounterButton, PassiveTreeButton
from framework.util.util import LEFT_CLICK, ORIGIN, SCREEN_RECT, quit_func

class Screen:
    INSTANCES = []

    @classmethod
    def get_instance(cls, name):
        return next((screen for screen in cls.INSTANCES if screen.name == name), None) 

    def __init__(self, name, surface, parent, screen_buttons, background_path=None):
        self.surface: pygame.surface.Surface = surface
        self.parent: Screen = parent 
        self.buttons: list[Button] = []
        self.name = name
        self.image = None

        if background_path:
            self.image = pygame.image.load(background_path)
            self.image = pygame.transform.scale(self.image, SCREEN_RECT)

        self._load_buttons()
        self._load_callbacks(screen_buttons)

        if self.back_button:
            self.back_button.click_rv = self.parent

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

    @property
    def back_button(self):
        try:
            return next(button for button in self.buttons if button.name == 'BackButton')
        except:
            return None

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
        if self.image:
            self.surface.blit(self.image, ORIGIN)
        else:
            self.surface.fill('black')

        last_click = None

        while True:
            if debug:
                for button in self.buttons:
                    button.draw(self.surface)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_func()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (clicked_button := next((button for button in self.buttons if button.checkForInput(mouse_pos)), None)):
                        if 'Temp-' in clicked_button.name:
                            clicked_button.name = input(f'Replacing {clicked_button.name}: ')
                        if clicked_button.click_rv:
                            return clicked_button.click_rv
                        if clicked_button.callback:
                            clicked_button.callback(mouse=event.button, screen=self)
                    elif debug:
                        if last_click:
                            self._add_new_button(last_click, mouse_pos)
                            last_click = None
                        else:
                            last_click = mouse_pos
                    else:
                        print(mouse_pos)

                if event.type == pygame.KEYUP:
                    nums = [eval(f'pygame.K_{i}') for i in range(10)]
                    if event.key in nums:
                        i = nums.index(event.key)
                        if i in range(len(self.buttons)): 
                            if self.buttons[i].click_rv:
                                return self.buttons[i].click_rv
                            if self.buttons[i].callback:
                                self.buttons[i].callback(mouse=LEFT_CLICK)
                        
            pygame.display.update()
    
    
    @classmethod
    def link_screens(cls):
        for screen_to_match in cls.INSTANCES:
            for button in screen_to_match.buttons:
                if (matching_screen := next((screen for screen in cls.INSTANCES if screen.name == button.name), None)):
                    button.click_rv = matching_screen
                    continue
    
    def __enter__(self):
        pass

    def __exit__(self):
        pass

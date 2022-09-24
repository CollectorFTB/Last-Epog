from framework.util.util import WHITE
from framework.util.font import font
from framework.util.util import blit_text

class Label:
    def __init__(self, rect, text):
        self.text = text 
        self.rect = rect
    
    def draw(self, surface, slide=False):
        if slide:
            blit_text(surface, self.text, self.rect, font(18), WHITE)
        else:
            text = font(self.rect.width//len(self.text)).render(self.text, True, WHITE)
            surface.blit(text, text.get_rect(center=self.rect.center))

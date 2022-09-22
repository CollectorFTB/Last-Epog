from framework.util.font import font

class Label:
    def __init__(self, text):
        self.text = text 
    
    def draw(self, surface):
        text = font(self.rect.width//len(self.text)).render(self.text, True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=self.rect.center))

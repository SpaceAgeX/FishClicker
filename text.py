import pygame

#Text class, Renders Text


class Text():
    

    def __init__(self, color, pos, size = 30):
        self.color = color
        self.pos = pos
        self.font = pygame.font.SysFont('arial', size)
        self.text = self.font.render("", 1, pygame.Color(self.color))

    def renderText(self, text, screen, pos):
        font = pygame.font.SysFont('arial', 30)
        self.text = self.font.render(text, 1, pygame.Color(self.color))
        screen.blit(self.text, pos)


class ToolTip():
    

    def __init__(self, area, size, color, text):
        self.area = area
        self.size = size
        self.color = color
        self.text = text
        self.textBox = Text((255, 255, 255), (0,0), 15)
    
    def update(self, area, size, color, text):
        self.area = area
        self.size = size
        self.color = color
        self.text = text
    
    def draw(self, surface, pos):

        pygame.draw.rect(surface, self.color, ((pos),(self.size)))
        self.textBox.renderText(self.text, surface, (pos[0], pos[1]+5))

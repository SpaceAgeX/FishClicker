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

    def render_multi_line(self, text, surface, x, y, fsize):
        lines = text.splitlines()
        font = pygame.font.SysFont('arial', fsize)
        for i, l in enumerate(lines):
            surface.blit(font.render(l, 1, pygame.Color(self.color)), (x, y + fsize*i))


class ToolTip():
    

    def __init__(self, area, size, color, text):
        self.area = area
        self.size = size
        self.color = color
        self.text = text
        self.textBox = Text((255, 255, 255), (0,0), 18)
    
    def update(self,factory):
        self.text = "Clicks: " + str(int(factory.price)) + "\nRate: " + str(int(factory.rate)) + "\nAmount: " + str(factory.count)
    
    def draw(self, surface, pos):

        pygame.draw.rect(surface, self.color, ((pos),(self.size)))
        self.textBox.render_multi_line(self.text, surface, pos[0]+ 15, pos[1]+5, 20)

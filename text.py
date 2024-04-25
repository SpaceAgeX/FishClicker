import pygame

#Text class, Renders Text


class Text():
    

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.font = pygame.font.SysFont('arial', 30)
        self.text = self.font.render("", 1, pygame.Color(self.color))

    def renderText(self, text, screen, pos):
        font = pygame.font.SysFont('arial', 30)
        self.text = self.font.render(text, 1, pygame.Color(self.color))
        screen.blit(self.text, pos)
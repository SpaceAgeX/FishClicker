import pygame

#Button class draws button at pos, returns true when pressed

class Button():
	def __init__(self, x, y, image, scale, tooltip):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.tooltip = tooltip

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
			self.tooltip.draw(surface, pos)

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		
		return action
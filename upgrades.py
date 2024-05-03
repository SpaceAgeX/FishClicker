import pygame
import random





class UpgradeData():
	upgradeType = [0, 1, 2, 3]
	upgradeValue = [1.125, 1.25, 1.5, 2]
	upgradePriceMult = [2, 2.5, 4, 5]# Times Initial Price

class Upgrades():

	

		

	

	def __init__(self, pos, dimensions, images):
		self.pos = pos
		self.dimensions = dimensions

		self.images = images

		self.buttons = []

		self.refresh()

	def refresh(self):
		for x in self.buttons:
			for y in x:
				del y
		self.buttons = []

		for x in range(0, self.dimensions[1]):
			self.buttons.append([])
			for y in range(0, self.dimensions[0]):
				image = random.randint(0,3)
				button = UpgradeButton(((y*32)+self.pos[0]), (x*32+self.pos[1]), self.images[image], image, 1, random.randint(0,3), 4)
				self.buttons[x].append(button)
		

	def draw(self, surface):
		value = (False, 0, 0)

		for x in range(0, self.dimensions[1]):
			for y in range(0, self.dimensions[0]):
				if self.buttons[x][y].draw(surface):
					value = (True, self.buttons[x][y].factory, self.buttons[x][y].frame)
					
		return value

		
		






class UpgradeButton():
	def __init__(self, x, y, image, factory, scale, frame, frames):
		width = image.get_width()
		height = image.get_height()
		self.frame = frame
		self.frames = frames
		self.factory = factory
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = pygame.Rect(x, y, self.image.get_width()/frames, self.image.get_height())
		self.clicked = False

	

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y), (self.frame*32, 0, 32, 32))

		return action




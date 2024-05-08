import pygame
import random
import text





class UpgradeData():
	upgradeType = [0, 1, 2, 3]
	upgradeValue = [1.125, 1.25, 1.5, 2]
	upgradePriceMult = [2, 2.5, 4, 8]# Times Initial Price
	upgradesUnlock = 100
	upgradeOpen = False

class Lock():


	def __init__(self, image):
		self.image = image
		self.rect = pygame.Rect(27, 80, self.image.get_width(), self.image.get_height())
		self.left = 100
		self.text = text.Text((255, 255, 255), (27+48, 80+64))
		self.unlocked = False
		self.clicked = False
	

	def draw(self, surface, left):

		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y), (0, 0, 96, 96))
		self.text.renderText(str(left), surface, ((27+48- self.text.text.get_width()/2, 80+64)))
		#check mouseover and clicked conditions
		
	

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
			

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		
		return action

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
				button = UpgradeButton(((y*32)+self.pos[0]), (x*32+self.pos[1]), self.images[image], image, 1, random.randint(0,3), 4, text.ToolTip(self.images[image].get_rect, (150, 75), (255,0,0), "This is a Tool Tip"))
				self.buttons[x].append(button)
		

	def draw(self, surface):
		value = (False, 0, 0)

		for x in reversed(range(0, self.dimensions[1])):
			for y in reversed(range(0, self.dimensions[0])):
				if self.buttons[x][y].draw(surface):
					value = (True, self.buttons[x][y].factory, self.buttons[x][y].frame)
					
		return value

		
		






class UpgradeButton():
	def __init__(self, x, y, image, factory, scale, frame, frames, tooltip):
		width = image.get_width()
		height = image.get_height()
		self.frame = frame
		self.frames = frames
		self.factory = factory
		self.tooltip = tooltip
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = pygame.Rect(x, y, self.image.get_width()/frames, self.image.get_height())
		self.clicked = False

	

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y), (self.frame*32, 0, 32, 32))

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
			self.tooltip.draw(surface, pos)

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		

		return action




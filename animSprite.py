import pygame
import datetime

class AnimSprite():
	

	def __init__(self, image, frames):
		self.image = image
		self.frames = frames
		self.frame = 0

	def draw(self, pos, surface, frame):
		surface.blit(self.image, pos, (frame*(self.image.get_width()/self.frames), 0, 64, 64))
		

class AnimSync():

	def __init__(self, timeInterval, frames):
		self.timeInterval= timeInterval
		self.frames = frames -1
		self.frame = 0
		self.timestart = datetime.datetime.now()


	def update(self):
		if (datetime.datetime.now() - self.timestart).total_seconds() > self.timeInterval:
			if self.frames != self.frame:
				self.frame += 1

			else:
				self.frame = 0

			self.timestart = datetime.datetime.now()
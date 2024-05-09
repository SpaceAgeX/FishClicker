import pygame



class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = []

    def push(self, st):
        if len(self.ls) == self.max_length:
            del self.ls[0]
            self.ls.pop(0)
        self.ls.append(st)

    def get_list(self):
        return self.ls







class Click():

	particles = MaxSizeList(20)

	def add(image):
		Click.particles.push(ClickParticle(image, pygame.mouse.get_pos(), (0, -1)))
	def draw(surface, pos, image):
		

		for i in Click.particles.get_list():
			i.draw(surface)


class ClickParticle():

	def __init__(self, image, pos, vel):
		self.image = image
		self.pos = pos
		self.start = pos[1]
		self.vel = vel
		self.range = 100
		self.alpha = 255
	def draw(self, surface):
		
		if self.pos[1] >= self.start-self.range:
			self.image.set_alpha(self.alpha)
			if self.image != None:
				surface.blit(self.image, self.pos)
				self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])
				self.alpha -= 4
		




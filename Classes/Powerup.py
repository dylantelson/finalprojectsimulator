import random
import pygame
from pygame.locals import *



class Powerup(pygame.sprite.Sprite):
	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		self.type = random.choice(["chair", "gravity"])
		if self.type == "chair":
			self.image = pygame.image.load('sprites/chair.png').convert_alpha()
		elif self.type == "gravity":
			self.image = pygame.image.load('sprites/gravity.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos


	def always(self, speed):
		self.x -= speed
		self.rect.topleft = (self.x, self.y)
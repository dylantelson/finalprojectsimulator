import random
import pygame
from pygame.locals import *

class MainCharacter(pygame.sprite.Sprite):
	def __init__(self, pos):

		self.gravity = 0.9
		self.gravitymultiplier = 1
		self.speed = 6
		self.maxspeed = 12
		self.yspeed = 1
		self.maxyspeed = 6
		self.x = pos[0]
		self.y = pos[1]
		self.dead = False
		self.image = pygame.image.load('sprites/player/run/run1.gif').convert_alpha()
		self.currentanim = 0
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.jumpforce = -11
		self.animcooldown = 1.5
		self.onGround = False
		self.runanims = [pygame.image.load('sprites/player/run/run1.gif').convert_alpha(), pygame.image.load('sprites/player/run/run2.gif').convert_alpha(), pygame.image.load('sprites/player/run/run3.gif').convert_alpha(), pygame.image.load('sprites/player/run/run4.gif').convert_alpha(), pygame.image.load('sprites/player/run/run5.gif').convert_alpha(), pygame.image.load('sprites/player/run/run6.gif').convert_alpha(), pygame.image.load('sprites/player/run/run7.gif').convert_alpha(), pygame.image.load('sprites/player/run/run8.gif').convert_alpha()]

	def always(self, buildings, powerups):

		self.onGround = False
		for i in range(len(buildings)):
			if pygame.sprite.collide_rect(self, buildings[i]):
				if self.y + 40 > buildings[i].y:
					self.speed = -0.3
					self.yspeed = 14
					self.dead = True
				else:
					self.onGround = True
					self.yspeed = 0
				break

		if self.yspeed < self.maxyspeed and not self.onGround:
			self.yspeed += self.gravity * self.gravitymultiplier
		self.y += self.yspeed
		self.animcooldown -= 1
		if self.animcooldown < 0:
			if self.onGround == True:
				if self.currentanim == len(self.runanims) - 1:
					self.currentanim = 0
				else:
					self.currentanim += 1
				self.image = self.runanims[self.currentanim]
			self.animcooldown = 1.5
		if self.speed < self.maxspeed:
				self.speed *= 1.001
		self.rect.topleft = (self.x, self.y)




	def jump(self):
		if self.onGround:
			self.y -= 10
			self.yspeed = self.jumpforce
			self.onGround = False
			self.rect.topleft = (self.x, self.y)

	def reset(self, pos):
		self.gravity = 0.9
		self.gravitymultiplier = 1
		self.speed = 6
		self.maxspeed = 12
		self.yspeed = 1
		self.maxyspeed = 6
		self.x = pos[0]
		self.y = pos[1]
		self.dead = False
		self.rect.topleft = (self.x, self.y)

	
class Floor(pygame.sprite.Sprite):
	def __init__(self, pos, width):



		self.width = width
		self.image = pygame.Surface((self.width,500))
		self.image.fill((random.choice([(0,0,0), (50,50,50), (32,32,32)])))
		self.x = pos[0]
		self.y = pos[1]
		self.rect = self.image.get_rect()
		self.rect.topleft = pos


	def always(self, speed):
		self.x -= speed
		self.rect.topleft = (self.x, self.y)

	def reset(self, floornum, y):
		if floornum == 0:
			self.x = 50
		elif floornum == 1:
			self.x = 300
		elif floornum == 2:
			self.x = 550
		elif floornum == 3:
			self.x = 800
		self.width = 200
		self.y = y
		self.image = pygame.Surface((self.width,500))
		self.image.fill((random.choice([(0, 0, 0), (50, 50, 50), (32, 32, 32)])))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)

		


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


import random
import pygame
from pygame.locals import *

class MainCharacter(pygame.sprite.Sprite):
	def __init__(self, pos):

		self.gravity = 0.05
		self.yspeed = 1
		self.x = pos[0]
		self.y = pos[1]
		self.speed = 2
		self.image = pygame.image.load('sprites/run1.gif').convert_alpha()
		self.currentanim = "run1"
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.jumpforce = -10
		self.animtime = 3
		self.onGround = False

	def always(self):

		global loop

		self.onGround = False
		if pygame.sprite.collide_rect(self, floor):
			if self.y + 40 > floor.y:
				self.speed = -0.3
				self.yspeed = 14
			else:
				self.onGround = True
				self.yspeed = 0
		elif pygame.sprite.collide_rect(self, floor2):
			if self.y + 40 > floor2.y:
				self.speed = -0.3
				self.yspeed = 14
			else:
				self.onGround = True
				self.yspeed = 0
		elif pygame.sprite.collide_rect(self, floor3):
			if self.y + 40 > floor3.y:
				self.speed = -0.3
				self.yspeed = 14
			else:
				self.onGround = True
				self.yspeed = 0
		elif pygame.sprite.collide_rect(self, floor4):
			if self.y + 40 > floor4.y:
				self.speed = -0.3
				self.yspeed = 14
			else:
				self.onGround = True
				self.yspeed = 0
		else:
			self.onGround = False
			self.yspeed += self.gravity
		if self.yspeed < 3 and not self.onGround:
			self.yspeed += 0.5
		self.y += self.yspeed
		self.animtime -= 1
		if self.animtime < 0:
			if self.onGround == True:
				if self.currentanim == "run1":
					self.image = run2
					self.currentanim = "run2"
				else:
					self.image = run1
					self.currentanim = "run1"
			self.animtime = 3
		if self.speed < 8:
				self.speed *= 1.001
		self.rect.topleft = (self.x, self.y)
		if self.y > 480:
			loop = False


	def jump(self):
		if self.onGround:
			self.y -= 6
			self.yspeed = self.jumpforce
			self.onGround = False
			self.rect.topleft = (self.x, self.y)
	
class Floor(pygame.sprite.Sprite):
	def __init__(self, pos):
		self.image = pygame.Surface((150,500))
		self.image.fill((50,50,50))
		self.x = pos[0]
		self.y = pos[1]
		self.rect = self.image.get_rect()
		self.rect.topleft = pos

	def always(self):
		self.x -= runnerboy.speed
		self.rect.topleft = (self.x, self.y)


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Parkour Simulator 2017")
clock = pygame.time.Clock()

run1 = pygame.image.load('sprites/run1.gif')
run2 = pygame.image.load('sprites/run2.gif')
screen_width = 640
screen_height = 480


screen = pygame.display.set_mode([screen_width, screen_height])
runnerboy = MainCharacter((50, 40))

randomfloory = 100

floor = Floor((50, randomfloory))
randomfloory += random.randint(-50, 50)
if randomfloory >= 420:
	randomfloory = 420
elif randomfloory <= 60:
	randomfloory = 60
floor2 = Floor((250, randomfloory))
randomfloory += random.randint(-50, 50)
if randomfloory >= 420:
	randomfloory = 420
elif randomfloory <= 60:
	randomfloory = 60
floor3 = Floor((450, randomfloory))
randomfloory += random.randint(-50, 50)
if randomfloory >= 420:
	randomfloory = 420
elif randomfloory <= 60:
	randomfloory = 60
floor4 = Floor((650, randomfloory))


loop = True
while loop:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				runnerboy.jump()
		if event.type == pygame.QUIT:
			loop = False
	if floor.x + 150 < 0:
		randomfloory += random.randint(-50, 50)
		floor = Floor((700, randomfloory))
	elif floor2.x + 150 < 0:
		randomfloory += random.randint(-50, 50)
		floor2 = Floor((700, randomfloory))
	elif floor3.x + 150 < 0:
		randomfloory += random.randint(-50, 50)
		floor3 = Floor((700,randomfloory))
	elif floor4.x + 150 < 0:
		randomfloory += random.randint(-50, 50)
		floor4 = Floor((700,randomfloory))
	screen.fill((100,100,100))
	floor.always()
	screen.blit(floor.image, (floor.x, floor.y))
	floor2.always()
	screen.blit(floor2.image, (floor2.x, floor2.y))
	floor3.always()
	screen.blit(floor3.image, (floor3.x, floor3.y))
	floor4.always()
	screen.blit(floor4.image, (floor4.x, floor4.y))
	runnerboy.always()
	screen.blit(runnerboy.image, (runnerboy.x, runnerboy.y))
	#pygame.draw.rect(sprite, (30,100,30), [rect.x, rect.y, 20, 20])
	pygame.display.update()
	clock.tick(60)


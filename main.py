import random
import modules
import pygame
import time
from pygame.locals import *

class ClassController():

	def __init__(self):
		pygame.init()
		pygame.font.init()
		font = pygame.font.SysFont('Comic Sans MS', 22)
		pygame.mixer.init()
		pygame.display.set_caption("Parkour Simulator 2017")
		clock = pygame.time.Clock()

		self.screen_width = 640
		self.screen_height = 480


		self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
		self.runnerboy = modules.MainCharacter((50, 249))

		self.randomfloory = 300
		self.randomwidth = 200

		self.floors = [modules.Floor((50, self.randomfloory), self.randomwidth)]
		for i in range(3):
			self.floors.append(modules.Floor((300 + 250 * i, self.randomfloory), self.randomwidth))

		self.powerups = []
		self.powerupscooldown = 0

		self.score = 0


		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.runnerboy.jump()
					elif event.key == pygame.K_DOWN:
						self.runnerboy.maxyspeed = 7
						self.runnerboy.gravitymultiplier = 5
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN:
						if self.powerupscooldown > 0:
							self.runnerboy.gravitymultiplier = 0.5
						else:
							self.runnerboy.gravitymultiplier = 1
						self.runnerboy.maxyspeed = 6

				if event.type == pygame.QUIT:
					loop = False

			for i in range(len(self.floors)):
				if self.floors[i].x + self.floors[i].width < 0:
					self.randomfloory += random.randint(-50, 50)
					if self.randomfloory >= 420:
						self.randomfloory = 420
					elif self.randomfloory <= 60:
						self.randomfloory = 60
					randomwidth = random.randint(150,350)
					if i == 0:
						self.floors[i] = modules.Floor((self.floors[len(self.floors)-1].x + self.floors[i - 1].width + 50, self.randomfloory), randomwidth)
					else:
						self.floors[i] = modules.Floor((self.floors[i - 1].x + self.floors[i - 1].width + 50, self.randomfloory), randomwidth)
					if random.randint(0,2) == 1:
						self.powerups.append(modules.Powerup((self.floors[i].x + self.floors[i].width / 2 - 31, self.randomfloory - 43)))

			self.screen.fill((100,100,100))

			speed = self.runnerboy.speed

			if self.powerupscooldown > 0:
				self.powerupscooldown -= 1
				if self.powerupscooldown <= 0:
					self.runnerboy.gravitymultiplier = 1


			for i in range(len(self.floors)):
				self.floors[i].always(speed)
				self.screen.blit(self.floors[i].image, (self.floors[i].x, self.floors[i].y))

			for i in range(len(self.powerups)):
				self.powerups[i].always(speed)
				self.screen.blit(self.powerups[i].image, (self.powerups[i].x, self.powerups[i].y))
				if pygame.sprite.collide_rect(self.runnerboy, self.powerups[i]):
					if self.powerups[i].type == "chair":
						self.runnerboy.speed -= 1
						del self.powerups[i]
					elif self.powerups[i].type == "gravity":
						self.runnerboy.gravitymultiplier = 0.5
						del self.powerups[i]
						self.powerupscooldown = 150
					if len(self.powerups) > 0:
						for i in range(i, len(self.powerups)):
							self.powerups[i].always(speed)
							self.screen.blit(self.powerups[i].image, (self.powerups[i].x, self.powerups[i].y))
					break
				if self.powerups[i].x + 62 < 0:
					del self.powerups[i]
					if len(self.powerups) > 0:
						for i in range(i, len(self.powerups)):
							self.powerups[i].always(speed)
							self.screen.blit(self.powerups[i].image, (self.powerups[i].x, self.powerups[i].y))
					break

			self.runnerboy.always(self.floors,self.powerups)
			self.screen.blit(self.runnerboy.image, (self.runnerboy.x, self.runnerboy.y))

			if self.runnerboy.y > 480:
				self.reset()
			if not self.runnerboy.dead:
				self.score += int(speed // 4)

			self.scoretext = font.render((str(('Score: ' + str(self.score)))), True, (0,0,0))
			self.screen.blit(self.scoretext, (10, 10))

			if self.powerupscooldown > 0:
				self.screen.blit(font.render(('Gravity: ' + str(self.powerupscooldown)), True, (0,0,0)), (10, 25))

			pygame.display.update()
			clock.tick(60)

	def reset(self):
		self.runnerboy.reset((50, 249))
		self.randomfloory = 300
		for i in range(len(self.floors)):
			if i > 0:
				self.randomfloory += random.randint(-50, 50)
			self.floors[i].reset(i, self.randomfloory)
		self.powerups = []
		self.powerupscooldown = 0
		self.score = 0


main = ClassController()

import random
import modules
import sys
import pygame
import time
from pygame.locals import *
from pygame.camera import *

class ClassController():

	def __init__(self):
		pygame.init()
		pygame.font.init()
		smallfont = pygame.font.SysFont('Comic Sans MS', 22)
		largefont = pygame.font.SysFont('Comic Sans MS', 30)
		pygame.mixer.init()
		pygame.display.set_caption("Parkour Simulator 2017")
		clock = pygame.time.Clock()
		camera = pygame.camera.Camera


		self.screen_width = 640
		self.screen_height = 480

		self.highscore = 0

		firstTime = True

		self.showmenu = True
		self.paused = False


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
					if event.key == pygame.K_SPACE and self.showmenu:
						self.showmenu = False
					elif event.key == pygame.K_ESCAPE:
						self.paused = True
					elif self.paused and event.key == pygame.K_c:
						self.paused = False
					elif self.paused and event.key == pygame.K_q:
						pygame.quit()
						sys.exit()
					elif event.key == pygame.K_UP:
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

			if self.showmenu:
				self.screen.fill((204,229,255))
				titletext = largefont.render(('Parkour Simulator 2017'), True, (0, 0, 0))
				self.screen.blit(titletext, (220, 100))


				pillimage = pygame.image.load('sprites/gravity.png').convert_alpha()
				chairimage = pygame.image.load('sprites/chair.png').convert_alpha()
				chairtext = smallfont.render(('Slows player on contact.'), True, (0,0,0))
				pilltext = smallfont.render(('Lowers the gravity of the player'), True, (0,0,0))
				highscoretext = smallfont.render((str(('High Score: ' + str(self.highscore)))), True, (0,0,0))
				tutorialtext = smallfont.render('Up on keyboard to jump, Down on keyboard to go down', True, (0,0,0))
				starttext = largefont.render('Press SPACE to start', True, (255,153,51))
				deathtext1 = largefont.render('YOU DIED', True, (0,0,0))
				deathtext2 = largefont.render('Press R to reset', True, (0,0,0))


				
				self.screen.blit(pillimage, (200, 190))
				self.screen.blit(pilltext, (250, 200) )
				self.screen.blit(chairimage, (205, 230))
				self.screen.blit(chairtext, (250, 250))
				self.screen.blit(highscoretext, (275, 350))
				self.screen.blit(tutorialtext, (150, 160))
				self.screen.blit(starttext, (220, 400))

			if self.paused:
				self.screen.fill((120,90,60))
				paused_text = largefont.render('Game paused, press C to continue or Q to quit', True, (0,0,0))
				self.screen.blit(paused_text, (120,100))


			elif not self.showmenu:

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

				self.screen.fill((254,91,53))

				speed = self.runnerboy.speed

				if self.powerupscooldown > 0:
					self.powerupscooldown -= 1
					if self.powerupscooldown <= 0:
						self.runnerboy.gravitymultiplier = 1
				'''
				xcoor = 0
				clouds = pygame.image.load('sprites/clouds.png').convert_alpha()
				rel_x = xcoor % clouds.get_rect().width
				self.screen.blit(clouds, (rel_x - clouds.get_rect().width, 0))
				if rel_x < self.screen_width:
					self.screen.blit(clouds, (rel_x, 0))
				xcoor -= 1
				#pygame.draw.line'''



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
					self.screen.fill((240,0,0))
					self.screen.blit(deathtext1, (220,100))
					self.screen.blit(deathtext2, (220,300))

					if self.score > self.highscore:
						self.highscore = self.score
					#self.reset()
					self.showmenu = True
				if not self.runnerboy.dead:
					self.score += int(speed // 4)

				self.scoretext = smallfont.render((str(('Score: ' + str(self.score)))), True, (0,0,0))
				self.screen.blit(self.scoretext, (10, 10))

				if self.powerupscooldown > 0:
					self.screen.blit(smallfont.render(('Gravity: ' + str(self.powerupscooldown)), True, (0,0,0)), (10, 25))

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